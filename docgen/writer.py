"""
Output writer module for the documentation generator.
"""

import os
from typing import Dict


class OutputWriter:
    """
    Write generated documentation to output files.
    """
    
    def __init__(self, output_dir: str):
        """
        Initialize the output writer.
        
        Args:
            output_dir: Directory to write documentation to
        """
        self.output_dir = output_dir
    
    def write(self, documentation: Dict[str, str]) -> None:
        """
        Write documentation to output files.
        
        Args:
            documentation: Dictionary of file paths to document content
        """
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Write each file
        for file_path, content in documentation.items():
            output_path = os.path.join(self.output_dir, file_path)
            
            # Create parent directories if needed
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)