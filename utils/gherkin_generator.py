"""
Gherkin generator module for converting callable docstrings into Gherkin feature files.
"""

import hashlib
import inspect
from datetime import datetime
from typing import Dict, Any, Callable, Optional, Tuple


class GherkinGenerator:
    """
    Generate Gherkin feature files from callable docstrings.
    
    This class provides functionality to convert Python callable docstrings
    into Gherkin feature files for behavior-driven documentation.
    """
    
    def __init__(self):
        """Initialize the Gherkin generator."""
        pass
    
    def make_gherkins(
        self, 
        callable_obj: Callable,
        docstring: Optional[str] = None,
        output_path: Optional[str] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate a Gherkin feature file from a callable's docstring.
        
        This function takes a callable (function, method, or class) and converts
        its docstring into a Gherkin feature file format. It extracts the description,
        parameters, return values, and examples to create comprehensive scenarios.
        
        Args:
            callable_obj: The callable object (function, method, or class) to document
            docstring: Optional docstring to use instead of extracting from callable
            output_path: Optional path where the feature file should be written
            
        Returns:
            Tuple containing:
                - str: The generated Gherkin feature file content
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
                    
        Raises:
            ValueError: If callable_obj is not a valid callable
            
        Examples:
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
            >>> generator = GherkinGenerator()
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
        
        # Generate Gherkin content
        gherkin_content = self._generate_gherkin_content(
            feature_name=feature_name,
            callable_name=callable_name,
            callable_signature=callable_signature,
            parsed_doc=parsed_doc
        )
        
        # Generate metadata
        metadata = self._generate_metadata(
            feature_name=feature_name,
            callable_name=callable_name,
            callable_signature=callable_signature,
            gherkin_content=gherkin_content,
            parsed_doc=parsed_doc,
            output_path=output_path
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
    
    def _generate_gherkin_content(
        self,
        feature_name: str,
        callable_name: str,
        callable_signature: str,
        parsed_doc: Dict[str, Any]
    ) -> str:
        """
        Generate the Gherkin feature file content.
        
        Args:
            feature_name: Name of the feature
            callable_name: Name of the callable
            callable_signature: Signature of the callable
            parsed_doc: Parsed docstring components
            
        Returns:
            Gherkin feature file content as string
        """
        lines = []
        
        # Feature header
        description = parsed_doc.get("description", "")
        if not description:
            description = f"Functionality of {callable_name}"
        
        lines.append(f"Feature: {feature_name}")
        lines.append(f"  As a user of the {callable_name} function")
        lines.append(f"  I want to use it according to its public contract")
        lines.append(f"  So that I can achieve the documented behavior")
        lines.append("")
        
        # Add description as comment
        if description:
            for desc_line in description.split('. '):
                if desc_line.strip():
                    lines.append(f"  # {desc_line.strip()}")
            lines.append("")
        
        # Background section with callable signature
        lines.append("  Background:")
        lines.append(f"    Given the callable '{callable_name}' with signature {callable_signature}")
        lines.append("    And the callable is accessible through the public API")
        lines.append("")
        
        # Main scenario - basic execution
        lines.append(f"  Scenario: Execute {callable_name} with valid inputs")
        
        # Add Given steps for parameters
        parameters = parsed_doc.get("parameters", [])
        if parameters:
            lines.append("    Given the following parameters are provided:")
            for param in parameters:
                param_name = param.get("name", "unknown")
                param_desc = param.get("description", "a value")
                lines.append(f"      | {param_name} | {param_desc} |")
        else:
            lines.append("    Given no parameters are required")
        
        # Add When step
        lines.append(f"    When I call {callable_name} with the provided parameters")
        
        # Add Then steps for return value
        returns = parsed_doc.get("returns", "")
        if returns:
            lines.append(f"    Then the function should return {returns}")
        else:
            lines.append("    Then the function should execute successfully")
        
        lines.append("    And all behavior should conform to the public contract")
        lines.append("")
        
        # Add scenario for error handling if raises are documented
        raises = parsed_doc.get("raises", [])
        if raises:
            lines.append(f"  Scenario: Handle error conditions in {callable_name}")
            lines.append("    Given invalid or edge case inputs are provided")
            lines.append(f"    When I call {callable_name} with invalid parameters")
            lines.append("    Then appropriate exceptions should be raised:")
            for raise_desc in raises:
                lines.append(f"      # {raise_desc}")
            lines.append("    And the error messages should be descriptive")
            lines.append("")
        
        # Add scenario outline if examples exist
        examples = parsed_doc.get("examples", [])
        if examples:
            lines.append(f"  Scenario Outline: Test {callable_name} with example inputs")
            if parameters:
                lines.append("    Given the following example inputs: <inputs>")
            lines.append(f"    When I execute {callable_name}")
            lines.append("    Then I should get the expected result: <output>")
            lines.append("")
            lines.append("    Examples:")
            lines.append("      | inputs | output |")
            for example in examples:
                # Simplified example representation
                lines.append(f"      | {example[:40]} | expected |")
            lines.append("")
        
        # Add verification scenario
        lines.append(f"  Scenario: Verify {callable_name} public contract")
        lines.append(f"    Given the {callable_name} callable is part of the public API")
        lines.append("    When I inspect its interface")
        lines.append("    Then all documented features should be accessible")
        lines.append("    And the behavior should match the documentation")
        lines.append("    And no internal implementation details should be exposed")
        
        return '\n'.join(lines)
    
    def _generate_metadata(
        self,
        feature_name: str,
        callable_name: str,
        callable_signature: str,
        gherkin_content: str,
        parsed_doc: Dict[str, Any],
        output_path: Optional[str] = None
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
        
        return {
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
            "description": parsed_doc.get("description", "")[:100]  # First 100 chars
        }


def make_gherkins(
    callable_obj: Callable,
    docstring: Optional[str] = None,
    output_path: Optional[str] = None
) -> Tuple[str, Dict[str, Any]]:
    """
    Generate a Gherkin feature file from a callable's docstring.
    
    This is a convenience function that creates a GherkinGenerator instance
    and calls its make_gherkins method. It provides a simple public API
    for generating Gherkin files from callable docstrings.
    
    Args:
        callable_obj: The callable object (function, method, or class) to document
        docstring: Optional docstring to use instead of extracting from callable
        output_path: Optional path where the feature file should be written
        
    Returns:
        Tuple containing:
            - str: The generated Gherkin feature file content
            - Dict[str, Any]: Metadata dictionary with information about the generation
            
    Raises:
        ValueError: If callable_obj is not a valid callable
        
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
        >>> content, metadata = make_gherkins(example_function)
        >>> assert 'Feature:' in content
        >>> assert metadata['callable_name'] == 'example_function'
    """
    generator = GherkinGenerator()
    return generator.make_gherkins(callable_obj, docstring, output_path)
