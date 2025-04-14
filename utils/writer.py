"""
Output writer module for the documentation generator.
"""

import os
from pathlib import Path
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
        self.output_dir = Path(output_dir) if output_dir else Path("docs")

        # Create output directory if it doesn't exist
        self.output_dir = self.output_dir.resolve()
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True, exist_ok=True)

    def write(self, documentation: Dict[str, str]) -> None:
        """
        Write documentation to output files.
        
        Args:
            documentation: Dictionary of file paths to document content
        """
        # Track existing files to avoid unnecessary overwrites
        existing_files = set()
        for path in self.output_dir.rglob('*'):
            if path.is_file():
                existing_files.add(path)

        # Write each file
        for file_path, content in documentation.items():
            # Convert string path to Path object
            output_path = self.output_dir / Path(file_path)

            # If "docs/docs/" is somewhere in the path, replace it with "docs/".
            if "docs/docs/" in str(output_path):
                output_path = Path(str(output_path).replace("docs/docs/", "docs/"))
            
            # Ensure directory structure exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Check if file exists and content is the same
            if output_path in existing_files:
                try:
                    existing_content = output_path.read_text(encoding='utf-8')
                    
                    # Skip writing if content hasn't changed
                    if existing_content == content:
                        continue
                except (IOError, UnicodeDecodeError):
                    # If we can't read the file, overwrite it
                    pass
            
            # Write content
            output_path.write_text(content, encoding='utf-8')
        
        # Remove empty directories that may have been created in output_dir.
        for path in self.output_dir.rglob('*'):
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
                print(f"Removed empty directory: {path}")
