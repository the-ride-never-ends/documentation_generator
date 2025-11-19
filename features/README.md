# Make Gherkins Feature

This directory contains Gherkin feature files for the documentation generator, including the `make_gherkins` feature itself.

## Overview

The `make_gherkins` feature converts Python callable docstrings into Gherkin feature files using LLM-powered generation with iterative refinement to ensure clarity and specificity.

## Requirements

- Python 3.6+
- OpenAI API key
- `openai` package: `pip install openai`

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

# Generate Gherkin feature file with OpenAI API
content, metadata = make_gherkins(
    example_function,
    api_key="sk-your-api-key-here"  # Or set OPENAI_API_KEY environment variable
)

# Content is the LLM-generated Gherkin feature file
print(content)

# Metadata contains information about the generation
print(metadata['feature_name'])     # Example Function
print(metadata['num_scenarios'])    # Number of scenarios generated
print(metadata['llm_iterations'])   # LLM refinement iterations used
print(metadata['content_hash'])     # SHA256 hash of content
```

### Advanced Usage

```python
from utils import GherkinGenerator

# Create generator instance with configuration
generator = GherkinGenerator(
    api_key="sk-your-api-key-here",
    max_iterations=5  # Max refinement loops per scenario
)

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
- **llm_iterations**: Total number of LLM refinement iterations used
- **error**: Error message if generation failed (optional)

## LLM-Powered Generation

### Iterative Refinement Process

The generator uses a sophisticated three-LLM pipeline to ensure quality:

1. **Generator LLM (GPT-4)**: Creates initial Gherkin scenarios from docstring
2. **Classifier LLM (GPT-3.5-turbo)**: Evaluates if scenarios are clear and specific
3. **Editor LLM (GPT-3.5-turbo)**: Provides actionable feedback on unclear aspects
4. **Regenerator LLM (GPT-4)**: Incorporates feedback to improve scenarios

Each scenario goes through this loop up to `max_iterations` times until it's deemed clear.

### Clarity Criteria

Scenarios are judged "clear" if they:
- Use concrete, specific assertions (not vague terms like "executes successfully")
- Specify exact return values, data types, and formats
- Include verifiable, observable outcomes
- Avoid ambiguous statements

**Example:**
- ❌ Unclear: "Then the function should execute successfully"
- ✅ Clear: "Then the function should return a dictionary with keys: status, data, timestamp"

## Features

### Supported Docstring Elements

The generator supports:

- **Description**: Main function/method description
- **Parameters**: Function arguments with descriptions
- **Return Values**: Return type and description
- **Exceptions**: Raised exceptions with descriptions
- **Examples**: Code examples (converted to Scenario Outlines)

### Generated Gherkin Structure

Each generated feature file includes LLM-generated scenarios for:

1. **Feature Header**: Feature name and user story (LLM-generated for clarity)
2. **Background**: Callable signature and API access (LLM-generated)
3. **Main Scenario**: Basic execution with specific, verifiable assertions
4. **Error Scenario**: Error handling with concrete exception details (if documented)
5. **Examples Scenario**: Example-based tests with specific data (if provided)
6. **Verification Scenario**: Public contract verification with concrete checks

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

content, metadata = make_gherkins(add, api_key="sk-...")
# LLM generates clear scenarios like:
# "Then the function should return an integer equal to the sum of a and b"
# Not: "Then the function should execute successfully"
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

content, metadata = make_gherkins(multiply, api_key="sk-...")
# LLM generates Scenario Outline with specific test data
# Includes concrete expected values, not just "expected"
```

### Example 3: Function with Exception Handling

```python
def divide(a: float, b: float) -> float:
    """Divide a by b.
    
    Raises:
        ZeroDivisionError: If b is zero
    """
    return a / b

content, metadata = make_gherkins(divide, api_key="sk-...")
# LLM generates specific error scenarios:
# "Then a ZeroDivisionError should be raised with message 'division by zero'"
# Not: "Then appropriate exceptions should be raised"
```

## Error Handling

The generator handles errors gracefully:

```python
content, metadata = make_gherkins(my_function, api_key="invalid")
# content will be an error message string
# metadata['error'] will contain the error details
# No RuntimeError raised by outer function
```

## Integration with Documentation Generator

The `make_gherkins` feature can be integrated into the main documentation generator workflow to automatically generate Gherkin files alongside Markdown documentation. Requires OpenAI API key configuration.

## Testing

To verify the feature works correctly:

```python
from utils import make_gherkins

# Test basic functionality
def test_func():
    """Test function."""
    pass

content, metadata = make_gherkins(test_func, api_key="sk-...")
assert 'Feature:' in content
assert metadata['callable_name'] == 'test_func'
assert metadata['llm_iterations'] > 0
print("✓ make_gherkins is working correctly")
```

## Installation

```bash
pip install openai
```

Set your OpenAI API key:
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

Or pass it directly:
```python
make_gherkins(func, api_key="sk-your-api-key-here")

## License

Part of the documentation_generator project.
