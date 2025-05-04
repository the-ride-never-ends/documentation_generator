"""
Command-line interface for the documentation generator.
"""

import argparse
import os
from typing import List


from .logger import logger


def load_ignore_paths(file_path: str) -> List[str]:
    """
    Load ignore paths from a file.
    
    Args:
        file_path: Path to the file containing ignore paths
        
    Returns:
        List[str]: List of paths to ignore
    """
    if not os.path.exists(file_path):
        return []
        
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]


def save_ignore_paths(file_path: str, paths: List[str]) -> None:
    """
    Save ignore paths to a file.
    
    Args:
        file_path: Path to the file to save ignore paths
        paths: List of paths to ignore
    """
    with open(file_path, 'w') as f:
        f.write("# Paths to ignore when generating documentation\n")
        for path in paths:
            f.write(f"{path}\n")


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments

    """
    parser = argparse.ArgumentParser(
        prog="documentation_generator",
        description="Generate documentation from Python source code."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to Python file or directory to generate documentation from (type: str)."
    )

    parser.add_argument(
        "--output",
        default="./docs",
        help="Path to output directory for documentation (default: ./docs) (type: str)."
    )

    parser.add_argument(
        "--format",
        default="markdown",
        choices=["markdown"],
        help="Output format for documentation (default: markdown) (type: str)"
    )

    parser.add_argument(
        "--docstring-style",
        default="google",
        choices=["google", "numpy", "rest"],
        help="Docstring style to parse (default: google) (type: str)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output (default: True) (type: bool)"
    )

    parser.add_argument(
        "--ignore",
        nargs="*",
        default=[],
        help="Paths to ignore when generating documentation (default: []) (type: list[str])."
    )

    parser.add_argument(
        "--ignore-file",
        default=".docignore",
        help="Path to file containing paths to ignore (default: .docignore) (type: str)."
    )

    parser.add_argument(
        "--save-ignore",
        action="store_true",
        help="Save ignore paths to ignore file (Default: True) (type: bool)."
    )

    parser.add_argument(
        "--inheritance",
        action="store_true",
        help="Enable enhanced inheritance documentation with class hierarchies and method overrides. (Default: True) (type: bool)."
    )

    parser.add_argument(
        "--self-doc",
        action="store_false",
        help="Enable self-documentation mode for documenting this tool itself (Default: False) (type: bool)."
    )

    args = parser.parse_args()

    # Validate input path
    if not os.path.exists(args.input):
        parser.error(f"Input path does not exist: {args.input}")

    # Always put output in a 'docs' subdirectory of the specified output path
    args.output = os.path.join(args.output, "docs")

    # Load ignore paths from file if it exists
    file_ignore_paths = load_ignore_paths(args.ignore_file)

    # Combine ignore paths from file and command line
    args.ignore = file_ignore_paths + args.ignore

    # Save ignore paths if requested
    if args.save_ignore and args.ignore:
        save_ignore_paths(args.ignore_file, args.ignore)
        if args.verbose:
            logger.info(f"Saved ignore paths to {args.ignore_file}")

    return args
