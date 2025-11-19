"""
Gherkin generator module for converting callable docstrings into Gherkin feature files.
"""

import hashlib
import inspect
import json
from datetime import datetime
from typing import Dict, Any, Callable, Optional, Tuple, List

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class GherkinGenerator:
    """
    Generate Gherkin feature files from callable docstrings using LLM-powered generation.
    
    This class uses OpenAI's API to generate clear, specific, and verifiable Gherkin scenarios
    with an iterative refinement loop to ensure quality.
    """
    
    def __init__(self, api_key: Optional[str] = None, max_iterations: int = 3):
        """
        Initialize the Gherkin generator with OpenAI API configuration.
        
        Args:
            api_key: OpenAI API key. If None, will try to use OPENAI_API_KEY environment variable.
            max_iterations: Maximum number of refinement iterations for each section (default: 3)
            
        Raises:
            RuntimeError: If OpenAI package is not installed
        """
        if OpenAI is None:
            raise RuntimeError(
                "OpenAI package is required for GherkinGenerator. "
                "Install it with: pip install openai"
            )
        
        self.api_key = api_key
        self.max_iterations = max_iterations
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
    
    def make_gherkins(
        self, 
        callable_obj: Callable,
        docstring: Optional[str] = None,
        output_path: Optional[str] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate a Gherkin feature file from a callable's docstring using LLM-powered generation.
        
        This function uses OpenAI's API to generate clear, specific, and verifiable Gherkin scenarios.
        Each section is iteratively refined through a classifier and editor loop until it meets
        clarity standards (unambiguous, verifiable external behavior).
        
        Args:
            callable_obj: The callable object (function, method, or class) to document
            docstring: Optional docstring to use instead of extracting from callable
            output_path: Optional path where the feature file should be written
            
        Returns:
            Tuple containing:
                - str: The generated Gherkin feature file content (or error message on failure)
                - Dict[str, Any]: Metadata dictionary with information about the generation
                    - feature_name: Name of the feature
                    - feature_file_path: Path where file should be written
                    - creation_timestamp: ISO format timestamp of generation
                    - callable_name: Name of the callable
                    - callable_signature: Signature of the callable
                    - num_scenarios: Number of scenarios generated
                    - content_hash: SHA256 hash of the content
                    - has_examples: Whether examples were included
                    - has_parameters: Whether parameters were documented
                    - has_return: Whether return value was documented
                    - llm_iterations: Number of LLM refinement iterations used
                    - error: Error message if generation failed (optional)
                    
        Raises:
            ValueError: If callable_obj is not a valid callable
            
        Examples:
            >>> generator = GherkinGenerator(api_key="sk-...")
            >>> def sample_function(param1: str, param2: int) -> bool:
            ...     '''Sample function with parameters.
            ...     
            ...     Args:
            ...         param1: First parameter
            ...         param2: Second parameter
            ...         
            ...     Returns:
            ...         bool: Success status
            ...     '''
            ...     return True
            >>> content, metadata = generator.make_gherkins(sample_function)
            >>> print(metadata['feature_name'])
            Sample Function
        """
        # Validate callable
        if not callable(callable_obj):
            raise ValueError(f"{callable_obj} is not a callable object")
        
        # Extract callable information
        callable_name = self._get_callable_name(callable_obj)
        callable_signature = self._get_callable_signature(callable_obj)
        
        # Get docstring
        if docstring is None:
            docstring = inspect.getdoc(callable_obj) or ""
        
        # Parse docstring structure
        parsed_doc = self._parse_docstring(docstring)
        
        # Generate feature name from callable name
        feature_name = self._generate_feature_name(callable_name)
        
        # Try to generate Gherkin content using LLM
        try:
            gherkin_content, llm_iterations = self._generate_gherkin_with_llm(
                feature_name=feature_name,
                callable_name=callable_name,
                callable_signature=callable_signature,
                parsed_doc=parsed_doc
            )
            error_msg = None
        except Exception as e:
            # Return error message instead of raising for outer function
            error_msg = f"Failed to generate Gherkin with LLM: {str(e)}"
            gherkin_content = error_msg
            llm_iterations = 0
        
        # Generate metadata
        metadata = self._generate_metadata(
            feature_name=feature_name,
            callable_name=callable_name,
            callable_signature=callable_signature,
            gherkin_content=gherkin_content,
            parsed_doc=parsed_doc,
            output_path=output_path,
            llm_iterations=llm_iterations,
            error=error_msg
        )
        
        return gherkin_content, metadata
    
    @staticmethod
    def _get_callable_name(callable_obj: Callable) -> str:
        """
        Extract the name of the callable.
        
        Args:
            callable_obj: The callable object
            
        Returns:
            Name of the callable
        """
        if hasattr(callable_obj, '__name__'):
            return callable_obj.__name__
        elif hasattr(callable_obj, '__class__'):
            return callable_obj.__class__.__name__
        else:
            return str(callable_obj)
    
    @staticmethod
    def _get_callable_signature(callable_obj: Callable) -> str:
        """
        Extract the signature of the callable.
        
        Args:
            callable_obj: The callable object
            
        Returns:
            String representation of the callable's signature
        """
        try:
            sig = inspect.signature(callable_obj)
            return str(sig)
        except (ValueError, TypeError):
            return "()"
    
    @staticmethod
    def _parse_docstring(docstring: str) -> Dict[str, Any]:
        """
        Parse docstring into structured components.
        
        Args:
            docstring: The docstring text
            
        Returns:
            Dictionary with parsed components:
                - description: Main description
                - parameters: List of parameters
                - returns: Return value description
                - examples: List of examples
        """
        if not docstring:
            return {
                "description": "",
                "parameters": [],
                "returns": "",
                "examples": [],
                "raises": []
            }
        
        lines = docstring.split('\n')
        result = {
            "description": [],
            "parameters": [],
            "returns": "",
            "examples": [],
            "raises": []
        }
        
        current_section = "description"
        current_param = None
        
        for line in lines:
            stripped = line.strip()
            
            # Detect section headers
            if stripped.lower().startswith(('args:', 'arguments:', 'parameters:')):
                current_section = "parameters"
                continue
            elif stripped.lower().startswith(('returns:', 'return:')):
                current_section = "returns"
                continue
            elif stripped.lower().startswith(('examples:', 'example:')):
                current_section = "examples"
                continue
            elif stripped.lower().startswith(('raises:', 'raise:')):
                current_section = "raises"
                continue
            
            # Parse content based on current section
            if current_section == "description" and stripped:
                result["description"].append(stripped)
            elif current_section == "parameters":
                # Simple parameter parsing (name: description)
                if ':' in stripped and not stripped.startswith(' '):
                    parts = stripped.split(':', 1)
                    param_name = parts[0].strip()
                    param_desc = parts[1].strip() if len(parts) > 1 else ""
                    current_param = {"name": param_name, "description": param_desc}
                    result["parameters"].append(current_param)
                elif current_param and stripped:
                    # Continue description of current parameter
                    current_param["description"] += " " + stripped
            elif current_section == "returns" and stripped:
                result["returns"] += " " + stripped if result["returns"] else stripped
            elif current_section == "examples" and stripped:
                result["examples"].append(stripped)
            elif current_section == "raises" and stripped:
                result["raises"].append(stripped)
        
        # Join description lines
        result["description"] = " ".join(result["description"])
        
        return result
    
    @staticmethod
    def _generate_feature_name(callable_name: str) -> str:
        """
        Generate a human-readable feature name from callable name.
        
        Args:
            callable_name: The name of the callable
            
        Returns:
            Human-readable feature name
        """
        # Convert snake_case to Title Case
        words = callable_name.replace('_', ' ').split()
        return ' '.join(word.capitalize() for word in words)
    
    def _generate_gherkin_with_llm(
        self,
        feature_name: str,
        callable_name: str,
        callable_signature: str,
        parsed_doc: Dict[str, Any]
    ) -> Tuple[str, int]:
        """
        Generate Gherkin content using LLM with iterative refinement.
        
        Args:
            feature_name: Name of the feature
            callable_name: Name of the callable
            callable_signature: Signature of the callable
            parsed_doc: Parsed docstring components
            
        Returns:
            Tuple of (gherkin_content, total_iterations)
            
        Raises:
            RuntimeError: If LLM generation fails
        """
        # Generate feature header
        feature_header = self._generate_feature_header_with_llm(
            feature_name, callable_name, parsed_doc
        )
        
        # Generate background section
        background = self._generate_background_with_llm(
            callable_name, callable_signature
        )
        
        # Generate main scenario
        main_scenario, main_iterations = self._refine_scenario_with_llm(
            scenario_type="main_execution",
            callable_name=callable_name,
            parsed_doc=parsed_doc
        )
        
        # Generate error scenario if needed
        error_scenario = ""
        error_iterations = 0
        if parsed_doc.get("raises"):
            error_scenario, error_iterations = self._refine_scenario_with_llm(
                scenario_type="error_handling",
                callable_name=callable_name,
                parsed_doc=parsed_doc
            )
        
        # Generate examples scenario if needed
        examples_scenario = ""
        examples_iterations = 0
        if parsed_doc.get("examples"):
            examples_scenario, examples_iterations = self._refine_scenario_with_llm(
                scenario_type="examples",
                callable_name=callable_name,
                parsed_doc=parsed_doc
            )
        
        # Generate verification scenario
        verification_scenario, verification_iterations = self._refine_scenario_with_llm(
            scenario_type="verification",
            callable_name=callable_name,
            parsed_doc=parsed_doc
        )
        
        # Combine all sections
        sections = [
            feature_header,
            background,
            main_scenario,
        ]
        
        if error_scenario:
            sections.append(error_scenario)
        
        if examples_scenario:
            sections.append(examples_scenario)
        
        sections.append(verification_scenario)
        
        gherkin_content = "\n\n".join(sections)
        
        total_iterations = (
            main_iterations + error_iterations + 
            examples_iterations + verification_iterations
        )
        
        return gherkin_content, total_iterations
    
    def _generate_feature_header_with_llm(
        self,
        feature_name: str,
        callable_name: str,
        parsed_doc: Dict[str, Any]
    ) -> str:
        """
        Generate feature header using LLM.
        
        Args:
            feature_name: Name of the feature
            callable_name: Name of the callable
            parsed_doc: Parsed docstring components
            
        Returns:
            Feature header text
            
        Raises:
            RuntimeError: If generation fails
        """
        description = parsed_doc.get("description", f"Functionality of {callable_name}")
        
        prompt = f"""Generate a Gherkin feature header for a function named '{callable_name}'.
        
Description: {description}

Create a clear, specific feature header with:
1. Feature: line with the feature name
2. User story (As a... I want... So that...)
3. Any relevant context as comments

The user story must describe verifiable external behavior, not vague statements.

Output only the feature header in valid Gherkin format."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at writing clear, specific Gherkin scenarios that describe unambiguous, verifiable external behavior."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to generate feature header: {str(e)}")
    
    def _generate_background_with_llm(
        self,
        callable_name: str,
        callable_signature: str
    ) -> str:
        """
        Generate background section using LLM.
        
        Args:
            callable_name: Name of the callable
            callable_signature: Signature of the callable
            
        Returns:
            Background section text
            
        Raises:
            RuntimeError: If generation fails
        """
        prompt = f"""Generate a Gherkin Background section for a callable named '{callable_name}' with signature: {callable_signature}

Create a clear Background section with:
1. Given step that establishes the callable exists and its signature
2. And step that confirms it's accessible through the public API

Output only the Background section in valid Gherkin format."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at writing clear, specific Gherkin scenarios."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to generate background: {str(e)}")
    
    def _refine_scenario_with_llm(
        self,
        scenario_type: str,
        callable_name: str,
        parsed_doc: Dict[str, Any]
    ) -> Tuple[str, int]:
        """
        Generate and refine a scenario using LLM with iterative feedback.
        
        This implements the refinement loop: generate → classify → edit → regenerate
        
        Args:
            scenario_type: Type of scenario (main_execution, error_handling, examples, verification)
            callable_name: Name of the callable
            parsed_doc: Parsed docstring components
            
        Returns:
            Tuple of (scenario_content, iterations_used)
            
        Raises:
            RuntimeError: If generation fails after max iterations
        """
        scenario = self._generate_scenario_with_llm(scenario_type, callable_name, parsed_doc)
        
        for iteration in range(self.max_iterations):
            # Classify if the scenario is clear
            is_clear, clarity_issues = self._classify_scenario_clarity(scenario)
            
            if is_clear:
                return scenario, iteration + 1
            
            # If not clear, get editor feedback
            editor_feedback = self._get_editor_feedback(scenario, clarity_issues)
            
            # Regenerate with editor feedback
            scenario = self._regenerate_scenario_with_feedback(
                scenario_type, callable_name, parsed_doc, editor_feedback
            )
        
        # If we've exhausted iterations and still not clear, raise error
        raise RuntimeError(
            f"Failed to generate clear scenario for {scenario_type} after {self.max_iterations} iterations"
        )
    
    def _generate_scenario_with_llm(
        self,
        scenario_type: str,
        callable_name: str,
        parsed_doc: Dict[str, Any]
    ) -> str:
        """
        Generate initial scenario using LLM.
        
        Args:
            scenario_type: Type of scenario
            callable_name: Name of the callable
            parsed_doc: Parsed docstring components
            
        Returns:
            Generated scenario text
            
        Raises:
            RuntimeError: If generation fails
        """
        prompts = {
            "main_execution": self._get_main_execution_prompt,
            "error_handling": self._get_error_handling_prompt,
            "examples": self._get_examples_prompt,
            "verification": self._get_verification_prompt
        }
        
        prompt_func = prompts.get(scenario_type)
        if not prompt_func:
            raise RuntimeError(f"Unknown scenario type: {scenario_type}")
        
        prompt = prompt_func(callable_name, parsed_doc)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at writing clear, specific Gherkin scenarios that describe unambiguous, verifiable external behavior. Avoid vague terms like 'executes successfully' - instead specify concrete, observable outcomes like 'returns a dictionary with keys: status, data'."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to generate scenario: {str(e)}")
    
    def _classify_scenario_clarity(self, scenario: str) -> Tuple[bool, List[str]]:
        """
        Use LLM to classify if a scenario is clear and specific.
        
        Args:
            scenario: The scenario text to classify
            
        Returns:
            Tuple of (is_clear, list_of_issues)
            
        Raises:
            RuntimeError: If classification fails
        """
        prompt = f"""Analyze this Gherkin scenario for clarity and specificity:

{scenario}

Evaluate if the scenario describes unambiguous, verifiable external behavior. Check for:
1. Vague terms like "executes successfully", "works correctly", "is valid"
2. Missing concrete return values or state changes
3. Ambiguous assertions that can't be objectively verified
4. Missing specific data types or formats

Respond in JSON format:
{{
    "is_clear": true/false,
    "issues": ["list of specific issues found"]
}}

If there are no issues, set is_clear to true and issues to empty list."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Gherkin quality classifier. You identify vague or ambiguous scenarios and require concrete, verifiable assertions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=300
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            return result["is_clear"], result.get("issues", [])
        except Exception as e:
            raise RuntimeError(f"Failed to classify scenario clarity: {str(e)}")
    
    def _get_editor_feedback(self, scenario: str, clarity_issues: List[str]) -> str:
        """
        Use LLM editor to provide specific feedback on unclear aspects.
        
        Args:
            scenario: The scenario text
            clarity_issues: List of identified issues
            
        Returns:
            Editor feedback text
            
        Raises:
            RuntimeError: If editor feedback fails
        """
        prompt = f"""You are an editor reviewing this Gherkin scenario:

{scenario}

The following clarity issues were identified:
{chr(10).join(f'- {issue}' for issue in clarity_issues)}

Provide specific, actionable feedback on how to make this scenario more clear and verifiable. Focus on:
1. Replacing vague terms with concrete, specific assertions
2. Adding specific data types, formats, or values
3. Making assertions objectively verifiable

Output your feedback as a list of specific improvements."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Gherkin editor who provides specific, actionable feedback to improve scenario clarity."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to get editor feedback: {str(e)}")
    
    def _regenerate_scenario_with_feedback(
        self,
        scenario_type: str,
        callable_name: str,
        parsed_doc: Dict[str, Any],
        editor_feedback: str
    ) -> str:
        """
        Regenerate scenario incorporating editor feedback.
        
        Args:
            scenario_type: Type of scenario
            callable_name: Name of the callable
            parsed_doc: Parsed docstring components
            editor_feedback: Feedback from editor
            
        Returns:
            Regenerated scenario text
            
        Raises:
            RuntimeError: If regeneration fails
        """
        prompts = {
            "main_execution": self._get_main_execution_prompt,
            "error_handling": self._get_error_handling_prompt,
            "examples": self._get_examples_prompt,
            "verification": self._get_verification_prompt
        }
        
        prompt_func = prompts.get(scenario_type)
        if not prompt_func:
            raise RuntimeError(f"Unknown scenario type: {scenario_type}")
        
        base_prompt = prompt_func(callable_name, parsed_doc)
        
        enhanced_prompt = f"""{base_prompt}

IMPORTANT: Incorporate this editor feedback to improve clarity:

{editor_feedback}

Generate an improved version with concrete, verifiable assertions."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at writing clear, specific Gherkin scenarios. You always incorporate feedback to make scenarios more concrete and verifiable."},
                    {"role": "user", "content": enhanced_prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to regenerate scenario: {str(e)}")
    
    def _get_main_execution_prompt(self, callable_name: str, parsed_doc: Dict[str, Any]) -> str:
        """Generate prompt for main execution scenario."""
        parameters = parsed_doc.get("parameters", [])
        returns = parsed_doc.get("returns", "")
        
        param_text = "\n".join([f"- {p['name']}: {p['description']}" for p in parameters])
        
        return f"""Generate a Gherkin scenario for the main execution path of '{callable_name}'.

Parameters:
{param_text if param_text else "None"}

Returns: {returns if returns else "Not specified"}

Create a scenario with:
1. Given steps for input parameters (specific values/types)
2. When step calling the function
3. Then step with CONCRETE return value (e.g., "returns a dictionary with keys: x, y, z" NOT "executes successfully")
4. Additional verifiable assertions

Output only the Scenario in valid Gherkin format with specific, verifiable assertions."""
    
    def _get_error_handling_prompt(self, callable_name: str, parsed_doc: Dict[str, Any]) -> str:
        """Generate prompt for error handling scenario."""
        raises = parsed_doc.get("raises", [])
        raises_text = "\n".join([f"- {r}" for r in raises])
        
        return f"""Generate a Gherkin scenario for error handling in '{callable_name}'.

Exceptions that can be raised:
{raises_text}

Create a scenario with:
1. Given steps for invalid inputs (be specific about what makes them invalid)
2. When step calling the function
3. Then step with SPECIFIC exception types and expected error messages
4. Verifiable assertions about error behavior

Output only the Scenario in valid Gherkin format with specific error conditions."""
    
    def _get_examples_prompt(self, callable_name: str, parsed_doc: Dict[str, Any]) -> str:
        """Generate prompt for examples scenario."""
        examples = parsed_doc.get("examples", [])
        examples_text = "\n".join([f"- {ex}" for ex in examples])
        
        return f"""Generate a Gherkin Scenario Outline for '{callable_name}' using these examples:

{examples_text}

Create a scenario outline with:
1. Given/When/Then steps with placeholders
2. Examples table with SPECIFIC input and output values
3. Concrete, verifiable expected results (not just "expected")

Output only the Scenario Outline in valid Gherkin format with specific test data."""
    
    def _get_verification_prompt(self, callable_name: str, parsed_doc: Dict[str, Any]) -> str:
        """Generate prompt for public contract verification scenario."""
        return f"""Generate a Gherkin scenario to verify the public contract of '{callable_name}'.

Create a scenario that verifies:
1. The callable is accessible via public API
2. Documented features are available
3. Behavior matches documentation
4. No internal implementation details exposed

Use SPECIFIC assertions like "the function signature matches <signature>" NOT vague terms like "features are accessible".

Output only the Scenario in valid Gherkin format with concrete verification steps."""
    
    def _generate_metadata(
        self,
        feature_name: str,
        callable_name: str,
        callable_signature: str,
        gherkin_content: str,
        parsed_doc: Dict[str, Any],
        output_path: Optional[str] = None,
        llm_iterations: int = 0,
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate metadata dictionary about the Gherkin generation.
        
        Args:
            feature_name: Name of the feature
            callable_name: Name of the callable
            callable_signature: Signature of the callable
            gherkin_content: Generated Gherkin content
            parsed_doc: Parsed docstring components
            output_path: Optional output path
            llm_iterations: Number of LLM refinement iterations used
            error: Error message if generation failed
            
        Returns:
            Metadata dictionary
        """
        # Calculate content hash
        content_hash = hashlib.sha256(gherkin_content.encode('utf-8')).hexdigest()
        
        # Count scenarios
        num_scenarios = gherkin_content.count('Scenario:') + gherkin_content.count('Scenario Outline:')
        
        # Determine output path
        if output_path is None:
            # Generate default path from callable name
            output_path = f"features/{callable_name}.feature"
        
        # Generate timestamp
        timestamp = datetime.now().isoformat()
        
        metadata = {
            "feature_name": feature_name,
            "feature_file_path": output_path,
            "creation_timestamp": timestamp,
            "callable_name": callable_name,
            "callable_signature": callable_signature,
            "num_scenarios": num_scenarios,
            "content_hash": content_hash,
            "has_examples": len(parsed_doc.get("examples", [])) > 0,
            "has_parameters": len(parsed_doc.get("parameters", [])) > 0,
            "has_return": bool(parsed_doc.get("returns", "")),
            "content_length": len(gherkin_content),
            "description": parsed_doc.get("description", "")[:100],  # First 100 chars
            "llm_iterations": llm_iterations
        }
        
        if error:
            metadata["error"] = error
        
        return metadata


def make_gherkins(
    callable_obj: Callable,
    docstring: Optional[str] = None,
    output_path: Optional[str] = None,
    api_key: Optional[str] = None,
    max_iterations: int = 3
) -> Tuple[str, Dict[str, Any]]:
    """
    Generate a Gherkin feature file from a callable's docstring using LLM-powered generation.
    
    This is a convenience function that creates a GherkinGenerator instance
    and calls its make_gherkins method. It provides a simple public API
    for generating Gherkin files from callable docstrings.
    
    Args:
        callable_obj: The callable object (function, method, or class) to document
        docstring: Optional docstring to use instead of extracting from callable
        output_path: Optional path where the feature file should be written
        api_key: OpenAI API key. If None, will try to use OPENAI_API_KEY environment variable.
        max_iterations: Maximum number of refinement iterations for each section (default: 3)
        
    Returns:
        Tuple containing:
            - str: The generated Gherkin feature file content (or error message on failure)
            - Dict[str, Any]: Metadata dictionary with information about the generation
            
    Raises:
        ValueError: If callable_obj is not a valid callable
        RuntimeError: If OpenAI package is not installed
        
    Examples:
        >>> def example_function(x: int) -> int:
        ...     '''Multiply x by 2.
        ...     
        ...     Args:
        ...         x: Input number
        ...         
        ...     Returns:
        ...         int: Result of x * 2
        ...     '''
        ...     return x * 2
        >>> content, metadata = make_gherkins(example_function, api_key="sk-...")
        >>> assert 'Feature:' in content
        >>> assert metadata['callable_name'] == 'example_function'
    """
    generator = GherkinGenerator(api_key=api_key, max_iterations=max_iterations)
    return generator.make_gherkins(callable_obj, docstring, output_path)
