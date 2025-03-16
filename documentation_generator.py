#!/usr/bin/env python3
"""
Documentation Generator - A tool to generate documentation from Python source code.

This module serves as the entry point for the documentation generator tool.
"""
import sys


from .utils.cli import parse_args
from .utils.file_processor import FileProcessor
from .utils.parser import CodeParser
from .utils.generator import DocumentationGenerator
from .utils.writer import OutputWriter


def main() -> int:
    """
    Main entry point for the documentation generator.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Parse command line arguments
    args = parse_args()
    
    # Process input files
    file_processor = FileProcessor(args.input)
    python_files = file_processor.find_python_files()
    
    # Parse source code
    parser = CodeParser()
    parsed_files = {}
    
    print(f"Processing {len(python_files)} Python files...")
    for file_path in python_files:
        try:
            result = parser.parse(file_path, docstring_style=args.docstring_style)
            parsed_files[file_path] = result
            if args.verbose:
                print(f"Processed: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}", file=sys.stderr)
    
    # Generate documentation
    generator = DocumentationGenerator(parsed_files)
    documentation = generator.generate(format=args.format)
    
    # Write output
    writer = OutputWriter(args.output)
    writer.write(documentation)
    
    print(f"Documentation generated successfully in {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())