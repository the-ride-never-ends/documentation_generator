"""
Command-line interface for the documentation generator.
"""

import argparse
import os


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed command-line arguments

    """
    parser = argparse.ArgumentParser(
        description="Generate documentation from Python source code."
    )
    
    parser.add_argument(
        "--input",
        required=True,
        help="Path to Python file or directory to generate documentation from"
    )
    
    parser.add_argument(
        "--output",
        default="./docs",
        help="Path to output directory for documentation (default: ./docs)"
    )
    
    parser.add_argument(
        "--format",
        default="markdown",
        choices=["markdown"],
        help="Output format for documentation (default: markdown)"
    )
    
    parser.add_argument(
        "--docstring-style",
        default="google",
        choices=["google", "numpy", "rest"],
        help="Docstring style to parse (default: google)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate input path
    if not os.path.exists(args.input):
        parser.error(f"Input path does not exist: {args.input}")
    
    return args