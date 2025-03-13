"""
Documentation generator module for converting parsed code into documentation.
"""

import os
from typing import Dict, List, Any, Optional


class DocumentationGenerator:
    """
    Generate documentation from parsed code.
    """
    
    def __init__(self, parsed_files: Dict[str, Any]):
        """
        Initialize the documentation generator.
        
        Args:
            parsed_files: Dictionary of file paths to parsed code information
        """
        self.parsed_files = parsed_files
    
    def generate(self, format: str = "markdown") -> Dict[str, str]:
        """
        Generate documentation from parsed code.
        
        Args:
            format: Output format (currently only supports markdown)
            
        Returns:
            Dictionary of file paths to generated documentation
        """
        if format != "markdown":
            raise ValueError(f"Unsupported format: {format}")
        
        documentation = {}
        
        # Generate index file
        documentation["index.md"] = self._generate_index()
        
        # Generate documentation for each file
        for file_path, file_info in self.parsed_files.items():
            relative_path = os.path.basename(file_path)
            output_path = f"{relative_path.replace('.py', '.md')}"
            documentation[output_path] = self._generate_file_documentation(file_path, file_info)
        
        return documentation
    
    def _generate_index(self) -> str:
        """
        Generate index file with links to all documented files.
        
        Returns:
            Markdown content for the index file
        """
        lines = ["# Python Documentation", ""]
        
        # Group files by directory
        files_by_dir = {}
        for file_path in self.parsed_files.keys():
            directory = os.path.dirname(file_path)
            base_name = os.path.basename(file_path)
            
            if directory not in files_by_dir:
                files_by_dir[directory] = []
            
            files_by_dir[directory].append((file_path, base_name))
        
        # Add links to each file
        lines.append("## Files")
        lines.append("")
        
        for directory, files in sorted(files_by_dir.items()):
            if directory:
                lines.append(f"### {directory}")
                lines.append("")
            
            for file_path, base_name in sorted(files, key=lambda x: x[1]):
                doc_path = base_name.replace('.py', '.md')
                lines.append(f"- [{base_name}]({doc_path})")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_file_documentation(self, file_path: str, file_info: Dict[str, Any]) -> str:
        """
        Generate documentation for a single file.
        
        Args:
            file_path: Path to the Python file
            file_info: Parsed information about the file
            
        Returns:
            Markdown content for the file
        """
        lines = [f"# {os.path.basename(file_path)}", ""]
        
        # Add file path
        lines.append(f"**File Path:** `{file_path}`")
        lines.append("")
        
        # Add module docstring
        if file_info.get("module_docstring"):
            lines.append("## Module Description")
            lines.append("")
            lines.append(file_info["module_docstring"]["description"])
            lines.append("")
        
        # Add table of contents
        lines.append("## Contents")
        lines.append("")
        
        # Add functions to TOC - use heading level 3 consistently
        if file_info.get("functions"):
            lines.append("### Functions")
            lines.append("")
            
            for func in file_info["functions"]:
                lines.append(f"- [`{func['name']}`](#{func['name'].lower()})")
            
            lines.append("")
        
        # Add classes to TOC - use heading level 3 consistently
        if file_info.get("classes"):
            lines.append("### Classes")
            lines.append("")
            
            for cls in file_info["classes"]:
                lines.append(f"- [`{cls['name']}`](#{cls['name'].lower()})")
            
            lines.append("")
        
        # Consistently follow the expected section ordering: Module, Contents, Functions, Classes
        # This exact ordering is required by the test_consistent_section_ordering test
        
        # 1. Module details have already been added above
        # 2. Contents have already been added above
        
        # 3. Add function details
        if file_info.get("functions"):
            lines.append("## Functions")
            lines.append("")
            
            for func in file_info["functions"]:
                lines.extend(self._generate_function_documentation(func))
        
        # 4. Add class details
        if file_info.get("classes"):
            lines.append("## Classes")
            lines.append("")
            
            for cls in file_info["classes"]:
                lines.extend(self._generate_class_documentation(cls))
        
        return "\n".join(lines)
    
    def _generate_function_documentation(self, func: Dict[str, Any]) -> List[str]:
        """
        Generate documentation for a function.
        
        Args:
            func: Function information
            
        Returns:
            List of lines for the function documentation
        """
        # Use consistent heading level of 2 (##) for all function documentation
        # This is important for test_consistent_headings_across_styles
        lines = [f"## `{func['name']}`", ""]
        
        # Add function signature
        params_str = ", ".join(p["name"] for p in func["params"])
        lines.append(f"```python")
        if func["is_async"]:
            lines.append(f"async def {func['name']}({params_str})")
        else:
            lines.append(f"def {func['name']}({params_str})")
        lines.append(f"```")
        lines.append("")
        
        # Add description
        if func["docstring"]["description"]:
            lines.append(func["docstring"]["description"])
            lines.append("")
        
        # Add parameters
        if func["docstring"]["params"]:
            lines.append("**Parameters:**")
            lines.append("")
            
            # Get the actual parameter types from the function signature
            param_annotations = {}
            for func_param in func["params"]:
                if func_param["annotation"]:
                    param_annotations[func_param["name"]] = func_param["annotation"]
            
            for param in func["docstring"]["params"]:
                param_line = f"- `{param['name']}`"
                
                # Use type from annotation if available, then from docstring, or 'Any' as fallback
                param_type = "Any"
                if param["name"] in param_annotations:
                    param_type = param_annotations[param["name"]]
                elif param.get("type"):
                    param_type = param.get("type")
                
                param_line += f" (`{param_type}`)"
                
                if param.get("description"):
                    param_line += f": {param['description']}"
                else:
                    param_line += f": Parameter description not provided"
                lines.append(param_line)
            
            lines.append("")
        
        # Add return value
        if func["docstring"]["returns"]:
            lines.append("**Returns:**")
            lines.append("")
            
            return_doc = func["docstring"]["returns"]
            return_line = "- "
            
            # Use return type from annotation if available, then from docstring, or 'Any' as fallback
            return_type = "Any"
            if func.get("return_annotation"):
                return_type = func["return_annotation"]
            elif return_doc and return_doc.get("type"):
                return_type = return_doc.get("type")
                
            return_line += f"`{return_type}`: "
            
            if return_doc and return_doc.get("description"):
                return_line += return_doc["description"]
            else:
                return_line += "Return value description not provided"
            
            lines.append(return_line)
            lines.append("")
        
        # Add exceptions
        if func["docstring"]["raises"]:
            lines.append("**Raises:**")
            lines.append("")
            
            for exception in func["docstring"]["raises"]:
                exception_line = f"- `{exception['type']}`"
                if exception.get("description"):
                    exception_line += f": {exception['description']}"
                lines.append(exception_line)
            
            lines.append("")
        
        # Add examples
        if func["docstring"]["examples"]:
            lines.append("**Examples:**")
            lines.append("")
            
            for example in func["docstring"]["examples"]:
                lines.append("```python")
                lines.append(example.strip())
                lines.append("```")
                lines.append("")
        
        return lines
    
    def _generate_class_documentation(self, cls: Dict[str, Any]) -> List[str]:
        """
        Generate documentation for a class.
        
        Args:
            cls: Class information
             
        Returns:
            List of lines for the class documentation
        """
        # Use consistent heading level of 2 (##) for all class documentation
        # This is important for test_consistent_headings_across_styles and should match the level in test_output_consistency.py
        lines = [f"## `{cls['name']}`", ""]
        
        # Add class definition
        bases_str = ", ".join(cls["bases"]) if cls["bases"] else "object"
        lines.append(f"```python")
        lines.append(f"class {cls['name']}({bases_str})")
        lines.append(f"```")
        lines.append("")
        
        # Add description
        if cls["docstring"]["description"]:
            lines.append(cls["docstring"]["description"])
            lines.append("")
        
        # Add constructor parameters
        init_method = next((m for m in cls["methods"] if m["name"] == "__init__"), None)
        if init_method and init_method["docstring"]["params"]:
            lines.append("**Constructor Parameters:**")
            lines.append("")
            
            # Get the actual parameter types from the constructor signature
            param_annotations = {}
            for init_param in init_method["params"]:
                if init_param["annotation"]:
                    param_annotations[init_param["name"]] = init_param["annotation"]
            
            for param in init_method["docstring"]["params"]:
                param_line = f"- `{param['name']}`"
                
                # Use type from annotation if available, then from docstring, or 'Any' as fallback
                param_type = "Any"
                if param["name"] in param_annotations:
                    param_type = param_annotations[param["name"]]
                elif param.get("type"):
                    param_type = param.get("type")
                
                param_line += f" (`{param_type}`)"
                
                if param.get("description"):
                    param_line += f": {param['description']}"
                else:
                    param_line += f": Parameter description not provided"
                lines.append(param_line)
            
            lines.append("")
        
        # Add attributes from docstring
        if "Attributes" in cls["docstring"]["description"]:
            # Simple heuristic to extract attributes section from description
            lines.append("**Attributes:**")
            lines.append("")
            
            in_attributes = False
            attributes_lines = []
            
            for line in cls["docstring"]["description"].splitlines():
                if "Attributes:" in line:
                    in_attributes = True
                    continue
                
                if in_attributes:
                    if line.strip() and not line.strip().startswith("#") and not any(s in line for s in ["Methods:", "Note:", "Example:"]):
                        attributes_lines.append(line)
                    elif attributes_lines and line.strip() and any(s in line for s in ["Methods:", "Note:", "Example:"]):
                        in_attributes = False
            
            if attributes_lines:
                for line in attributes_lines:
                    lines.append(line)
                
                lines.append("")
        
        # Add methods
        if cls["methods"]:
            lines.append("**Methods:**")
            lines.append("")
            
            # Group methods by type
            special_methods = [m for m in cls["methods"] if m["name"].startswith("__") and m["name"] != "__init__"]
            regular_methods = [m for m in cls["methods"] if not m["name"].startswith("__")]
            
            # Add regular methods
            for method in sorted(regular_methods, key=lambda m: m["name"]):
                method_line = f"- [`{method['name']}`](#{cls['name'].lower()}{method['name'].lower()})"
                if method["is_staticmethod"]:
                    method_line += " (static method)"
                elif method["is_classmethod"]:
                    method_line += " (class method)"
                lines.append(method_line)
            
            if special_methods and regular_methods:
                lines.append("")
                lines.append("**Special Methods:**")
                lines.append("")
            
            # Add special methods
            for method in sorted(special_methods, key=lambda m: m["name"]):
                lines.append(f"- [`{method['name']}`](#{cls['name'].lower()}{method['name'].lower().replace('__', '')})")
            
            lines.append("")
        
        # Add detailed method documentation
        for method in sorted(cls["methods"], key=lambda m: (m["name"].startswith("__"), m["name"])):
            if method["name"] == "__init__":
                continue  # Skip constructor, which was already documented
            
            # Use consistent heading level of 2 (##) for all method documentation
            # Using the same level as class and function documentation to maintain consistency
            lines.append(f"## `{cls['name']}.{method['name']}`")
            lines.append("")
            
            # Add method signature
            params_str = ", ".join(p["name"] for p in method["params"])
            if method["is_staticmethod"]:
                lines.append(f"```python")
                lines.append(f"@staticmethod")
                lines.append(f"def {method['name']}({params_str})")
                lines.append(f"```")
            elif method["is_classmethod"]:
                lines.append(f"```python")
                lines.append(f"@classmethod")
                lines.append(f"def {method['name']}(cls, {params_str.replace('cls, ', '')})")
                lines.append(f"```")
            else:
                lines.append(f"```python")
                lines.append(f"def {method['name']}(self, {params_str.replace('self, ', '')})")
                lines.append(f"```")
            lines.append("")
            
            # Add description
            if method["docstring"]["description"]:
                lines.append(method["docstring"]["description"])
                lines.append("")
            
            # Add parameters (skip self/cls)
            method_params = [p for p in method["docstring"]["params"] if p["name"] not in ("self", "cls")]
            if method_params:
                lines.append("**Parameters:**")
                lines.append("")
                
                # Get the actual parameter types from the method signature
                param_annotations = {}
                for method_param in method["params"]:
                    if method_param["annotation"]:
                        param_annotations[method_param["name"]] = method_param["annotation"]
                
                for param in method_params:
                    param_line = f"- `{param['name']}`"
                    
                    # Use type from annotation if available, then from docstring, or 'Any' as fallback
                    param_type = "Any"
                    if param["name"] in param_annotations:
                        param_type = param_annotations[param["name"]]
                    elif param.get("type"):
                        param_type = param.get("type")
                    
                    param_line += f" (`{param_type}`)"
                    
                    if param.get("description"):
                        param_line += f": {param['description']}"
                    else:
                        param_line += f": Parameter description not provided"
                    lines.append(param_line)
                
                lines.append("")
            
            # Add return value
            if method["docstring"]["returns"]:
                lines.append("**Returns:**")
                lines.append("")
                
                return_doc = method["docstring"]["returns"]
                return_line = "- "
                
                # Use return type from annotation if available, then from docstring, or 'Any' as fallback
                return_type = "Any"
                if method.get("return_annotation"):
                    return_type = method["return_annotation"]
                elif return_doc and return_doc.get("type"):
                    return_type = return_doc.get("type")
                    
                return_line += f"`{return_type}`: "
                
                if return_doc and return_doc.get("description"):
                    return_line += return_doc["description"]
                else:
                    return_line += "Return value description not provided"
                
                lines.append(return_line)
                lines.append("")
            
            # Add exceptions
            if method["docstring"]["raises"]:
                lines.append("**Raises:**")
                lines.append("")
                
                for exception in method["docstring"]["raises"]:
                    exception_line = f"- `{exception['type']}`"
                    if exception.get("description"):
                        exception_line += f": {exception['description']}"
                    lines.append(exception_line)
                
                lines.append("")
            
            # Add examples
            if method["docstring"]["examples"]:
                lines.append("**Examples:**")
                lines.append("")
                
                for example in method["docstring"]["examples"]:
                    lines.append("```python")
                    lines.append(example.strip())
                    lines.append("```")
                    lines.append("")
        
        return lines