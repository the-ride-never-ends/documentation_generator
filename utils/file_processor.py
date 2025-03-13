"""
File processing module for the documentation generator.
"""

import os
from typing import List


class FileProcessor:
    """
    Process files and directories to find Python files for documentation.
    """
    
    def __init__(self, input_path: str):
        """
        Initialize the file processor.
        
        Args:
            input_path: Path to input file or directory
        """
        self.input_path = input_path
    
    def find_python_files(self) -> List[str]:
        """
        Find all Python files in the input path.
        
        Returns:
            List[str]: List of paths to Python files
        """
        python_files = []
        
        if os.path.isfile(self.input_path):
            if self.input_path.endswith('.py'):
                python_files.append(self.input_path)
        else:
            # Walk the directory structure
            for root, _, files in os.walk(self.input_path):
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))
        
        return python_files