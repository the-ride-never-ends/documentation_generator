#!/usr/bin/env python3
"""
Documentation Generator - A tool to generate documentation from Python source code.

This module serves as the entry point for the documentation generator tool.
"""
import logging
import sys


from utils.cli import parse_args
from utils.file_processor import FileProcessor
from utils.parser import CodeParser
from utils.generator import DocumentationGenerator
from utils.writer import OutputWriter
from utils.logger import logger


def main() -> int:
    """
    Main entry point for the documentation generator.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Parse command line arguments
    args = parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Process input files
    file_processor = FileProcessor(args.input)
    python_files = file_processor.find_python_files()
    
    # Parse source code
    parser = CodeParser()
    parsed_files = {}
    
    logger.info(f"Processing {len(python_files)} Python files...")
    for file_path in python_files:
        try:
            # Enable inheritance resolution if the option is specified
            inheritance_enabled = getattr(args, 'inheritance', False)
            result = parser.parse(
                file_path, 
                docstring_style=args.docstring_style,
                resolve_inheritance=inheritance_enabled
            )
            parsed_files[file_path] = result
            
            logger.debug(f"Processed: {file_path}")
        except Exception as e:
            logger.exception(f"Error processing {file_path}: {str(e)}", file=sys.stderr)
    
    # Generate documentation
    generator = DocumentationGenerator(parsed_files)
    documentation = generator.generate(format=args.format)
    
    # Handle self-documentation mode
    self_doc_mode = getattr(args, 'self_doc', False)
    if self_doc_mode:
        # TODO Add special handling for self-documentation
        logger.info("Running in self-documentation mode...")
        # In self-documentation mode, we might want to add special headers or metadata
        
    # Write output
    writer = OutputWriter(args.output)
    writer.write(documentation)
    
    logger.info(f"Documentation generated successfully in {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())