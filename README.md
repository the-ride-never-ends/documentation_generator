# Documentation Generator
## Authors
- Claude 3.7 Sonnet, Kyle Rose
## Version 0.8.0

A Python CLI tool that parses Python codebases to generate structured documentation in Markdown format.
Also a test to see the instruction following abilities of Claude Code.

## Overview

Documentation Generator automatically extracts code structure, docstrings, and type annotations from Python source code to produce comprehensive documentation in Markdown format. It supports multiple docstring styles (Google, NumPy, and reStructuredText) and preserves type hints from source code annotations.

## Features

- **Multi-style docstring support**: Extract documentation from Google, NumPy, and reStructuredText style docstrings
- **Type hint extraction**: Extracts type annotations directly from Python source code
- **Complete code structure documentation**: Documents modules, classes, methods, and functions
- **Fast and memory-efficient**: Processes over 12 million lines of code per minute with minimal memory usage
- **Robust error handling**: Continues processing even with syntax errors or malformed docstrings
- **Consistent output formatting**: Standardized Markdown formatting with proper heading hierarchy
- **Easy navigation**: Generated documentation includes links between related sections
- **Path ignoring**: Ability to ignore specific paths when generating documentation to exclude virtual environments, build directories, etc.

## Usage

```bash
# Basic usage
python documentation_generator.py --input /path/to/code --output /path/to/docs

# Specify docstring style
python documentation_generator.py --input /path/to/code --output /path/to/docs --docstring-style google

# Ignore specific paths
python documentation_generator.py --input /path/to/code --output /path/to/docs --ignore /path/to/code/venv /path/to/code/.git

# Save ignore paths for future use
python documentation_generator.py --input /path/to/code --output /path/to/docs --ignore /path/to/code/venv --save-ignore

# Use a custom ignore file
python documentation_generator.py --input /path/to/code --output /path/to/docs --ignore-file /path/to/custom/ignore/file

# Get help
python documentation_generator.py --help
```

### Command-line Options

- `--input`: Path to Python file or directory to generate documentation from (required)
- `--output`: Path to output directory for documentation (default: ./docs)
- `--format`: Output format for documentation (default: markdown)
- `--docstring-style`: Docstring style to parse (default: google)
- `--verbose`: Enable verbose output
- `--ignore`: Paths to ignore when generating documentation (can specify multiple paths)
- `--ignore-file`: Path to file containing paths to ignore (default: .docignore)
- `--save-ignore`: Save ignore paths to ignore file

### Ignore File Format

The ignore file (default: `.docignore`) contains paths to ignore when generating documentation, one per line. Comments begin with `#`.

Example `.docignore` file:

```
# Virtual environment directories
venv/
env/
.env/

# Git directories
.git/

# Build directories
build/
dist/
```

## Project Structure

```
documentation_generator/
├── README.md                       # Project documentation
├── __init__.py                     # Root package initialization
├── utils/                          # Main package
│   ├── __init__.py                 # Package initialization 
│   ├── cli.py                      # Command-line interface and ignore path handling
│   ├── file_processor.py           # Finds Python files to process and handles ignore paths
│   ├── generator.py                # Generates Markdown documentation
│   ├── parser.py                   # AST parsing for code structure extraction
│   └── writer.py                   # Writes documentation to output files
└── documentation_generator.py      # Entry point script
```
