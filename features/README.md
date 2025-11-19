# Make Gherkins Feature

This directory contains Gherkin feature files for the documentation generator, including the `make_gherkins` feature itself.

## Overview

The `make_gherkins` feature converts Python callable docstrings into Gherkin feature files for behavior-driven documentation.

## Usage

### Basic Usage

```python
from utils import make_gherkins

def example_function(x: int, y: int) -> int:
    """Add two numbers.
    
    Args:
        x: First number
        y: Second number
        
    Returns:
        int: Sum of x and y
    """
    return x + y

# Generate Gherkin feature file
content, metadata = make_gherkins(example_function)

# Content is the Gherkin feature file as a string
print(content)

# Metadata contains information about the generation
print(metadata['feature_name'])  # Example Function
print(metadata['num_scenarios'])  # Number of scenarios generated
print(metadata['content_hash'])  # SHA256 hash of content
```

### Advanced Usage

```python
from utils import GherkinGenerator

# Create generator instance
generator = GherkinGenerator()

# Generate with custom output path
content, metadata = generator.make_gherkins(
    example_function,
    output_path="features/custom_path.feature"
)

# Generate using custom docstring (useful for testing)
custom_docstring = """Custom documentation.
Args:
    param: A parameter
Returns:
    Result value
"""
content, metadata = generator.make_gherkins(
    example_function,
    docstring=custom_docstring
)
```

## Metadata Dictionary

The metadata dictionary returned by `make_gherkins` contains:

- **feature_name**: Human-readable feature name
- **feature_file_path**: Suggested path for the feature file
- **creation_timestamp**: ISO format timestamp
- **callable_name**: Name of the callable
- **callable_signature**: Full signature of the callable
- **num_scenarios**: Number of scenarios generated
- **content_hash**: SHA256 hash for verification
- **has_examples**: Whether examples were included
- **has_parameters**: Whether parameters were documented
- **has_return**: Whether return value was documented
- **content_length**: Length of generated content in bytes
- **description**: First 100 characters of description

## Features

### Supported Docstring Elements

The generator supports:

- **Description**: Main function/method description
- **Parameters**: Function arguments with descriptions
- **Return Values**: Return type and description
- **Exceptions**: Raised exceptions with descriptions
- **Examples**: Code examples (converted to Scenario Outlines)

### Generated Gherkin Structure

Each generated feature file includes:

1. **Feature Header**: Feature name and user story
2. **Background**: Callable signature and API access
3. **Main Scenario**: Basic execution with valid inputs
4. **Error Scenario**: Error handling (if exceptions documented)
5. **Examples Scenario**: Example-based tests (if examples provided)
6. **Verification Scenario**: Public contract verification

### Public Contract Conformance

All generated features are designed to be:

- **Testable**: Through the public API only
- **Verifiable**: All scenarios map to public methods
- **Secure**: No internal implementation details exposed
- **Standard**: Compatible with standard Gherkin parsers

## Files in this Directory

- **make_gherkins.feature**: Specification of the make_gherkins feature requirements
- **make_gherkins_implementation.feature**: Self-generated Gherkin for the make_gherkins function
- **README.md**: This documentation file

## Examples

### Example 1: Simple Function

```python
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

content, metadata = make_gherkins(add)
# Generates a feature with 2 scenarios
```

### Example 2: Function with Examples

```python
def multiply(x: int, y: int) -> int:
    """Multiply two numbers.
    
    Examples:
        multiply(2, 3)  # Returns 6
        multiply(5, 4)  # Returns 20
    """
    return x * y

content, metadata = make_gherkins(multiply)
# Generates a feature with 3 scenarios (including Scenario Outline)
```

### Example 3: Function with Exception Handling

```python
def divide(a: float, b: float) -> float:
    """Divide a by b.
    
    Raises:
        ZeroDivisionError: If b is zero
    """
    return a / b

content, metadata = make_gherkins(divide)
# Generates a feature with 3 scenarios (including error handling)
```

## Integration with Documentation Generator

The `make_gherkins` feature can be integrated into the main documentation generator workflow to automatically generate Gherkin files alongside Markdown documentation.

## Testing

To verify the feature works correctly:

```python
from utils import make_gherkins

# Test basic functionality
def test_func():
    """Test function."""
    pass

content, metadata = make_gherkins(test_func)
assert 'Feature:' in content
assert metadata['callable_name'] == 'test_func'
print("✓ make_gherkins is working correctly")
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## License

Part of the documentation_generator project.
