"""
File processing module for the documentation generator.
"""

import os
from typing import List
import os.path


class FileProcessor:
    """
    Process files and directories to find Python files for documentation.
    """
    
    def __init__(self, input_path: str, ignore_paths: List[str] = None):
        """
        Initialize the file processor.
        
        Args:
            input_path: Path to input file or directory
            ignore_paths: List of paths to ignore when finding Python files
        """
        self.input_path = input_path
        self.ignore_paths = ignore_paths or []
    
    def should_ignore(self, path: str) -> bool:
        """
        Check if a path should be ignored.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if the path should be ignored, False otherwise
        """
        # Normalize paths to absolute paths for comparison
        abs_path = os.path.abspath(path)
        
        for ignore_path in self.ignore_paths:
            # Normalize ignore path to absolute path
            abs_ignore_path = os.path.abspath(ignore_path)
            
            # Check if the path is the ignore path or is a subdirectory of the ignore path
            if abs_path == abs_ignore_path or abs_path.startswith(abs_ignore_path + os.sep):
                return True
                
        return False
    
    def find_python_files(self) -> List[str]:
        """
        Find all Python files in the input path, excluding ignored paths.
        
        Returns:
            List[str]: List of paths to Python files
        """
        python_files = []
        
        if os.path.isfile(self.input_path):
            if self.input_path.endswith('.py') and not self.should_ignore(self.input_path):
                python_files.append(self.input_path)
        else:
            # Walk the directory structure
            for root, dirs, files in os.walk(self.input_path):
                # Skip ignored directories
                dirs[:] = [d for d in dirs if not self.should_ignore(os.path.join(root, d))]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.endswith('.py') and not self.should_ignore(file_path):
                        python_files.append(file_path)
        
        return python_files