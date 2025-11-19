# Tests for make_gherkins

This directory contains test stubs for the `make_gherkins` functionality.

## Structure

- **`test_make_gherkins.py`** - Test stubs mapping one-to-one with Gherkin scenarios
- **`conftest.py`** - Pytest configuration and shared fixtures
- **`__init__.py`** - Package initialization

## Test Design

Each test stub corresponds to exactly **one scenario** from `features/make_gherkins.feature`.

### Test Docstrings

Test docstrings are taken **directly from the Gherkin scenarios**, preserving the Given/When/Then structure:

```python
def test_generate_gherkin_from_simple_function_docstring(simple_function):
    """
    Scenario: Generate Gherkin from a simple function docstring
    
    Given a callable with a docstring containing description, parameters, and returns
    When I call make_gherkins with the callable's docstring
    Then a Gherkin feature file should be generated
    And the feature file should contain a Feature section with the description
    And the feature file should contain Scenarios derived from the parameters
    And a metadata dictionary should be returned
    And the metadata dictionary should contain creation timestamp
    And the metadata dictionary should contain content summary
    """
    pass
```

## Fixtures

### Test-Specific Fixtures (in test_make_gherkins.py)

- `gherkin_generator` - Provides a GherkinGenerator instance
- `simple_function` - Function with basic docstring
- `function_with_multiple_parameters` - Function with multiple parameters
- `function_with_examples` - Function with examples in docstring
- `class_method_with_docstring` - Class method with comprehensive docstring
- `callable_without_docstring` - Callable without documentation
- `callable_with_complete_docstring` - Callable with complete documentation

### Shared Fixtures (in conftest.py)

- `mock_openai_api` - Mock OpenAI API for testing without API calls
- `api_key` - API key for testing
- `max_iterations` - Default max iterations for testing

## Running Tests

### Install pytest

```bash
pip install pytest pytest-mock
```

### Run all tests

```bash
pytest tests/test_make_gherkins.py -v
```

### Run specific test

```bash
pytest tests/test_make_gherkins.py::test_generate_gherkin_from_simple_function_docstring -v
```

### Run with coverage

```bash
pip install pytest-cov
pytest tests/test_make_gherkins.py --cov=utils.gherkin_generator --cov-report=html
```

## Implementation Notes

All test functions currently contain only `pass` statements - these are **stubs** to be implemented.

When implementing tests:

1. **Use fixtures** to set up test data
2. **Mock OpenAI API** calls to avoid costs and network dependencies
3. **Assert on metadata** returned by make_gherkins
4. **Verify Gherkin content** matches expected structure
5. **Test error handling** for invalid inputs
6. **Validate public contract** conformance

## Example Implementation

```python
def test_generate_gherkin_from_simple_function_docstring(simple_function, api_key):
    """
    Scenario: Generate Gherkin from a simple function docstring
    ...
    """
    # When
    content, metadata = make_gherkins(simple_function, api_key=api_key)
    
    # Then
    assert 'Feature:' in content
    assert metadata['feature_name'] is not None
    assert 'creation_timestamp' in metadata
    assert metadata['callable_name'] == 'simple_function'
```

## Mocking OpenAI API

To avoid API costs during testing, mock the OpenAI client:

```python
from unittest.mock import Mock, patch

@pytest.fixture
def mock_openai_client(mocker):
    mock_client = mocker.patch('utils.gherkin_generator.OpenAI')
    mock_response = Mock()
    mock_response.choices[0].message.content = "Feature: Test\n..."
    mock_client.return_value.chat.completions.create.return_value = mock_response
    return mock_client
```

## Test Coverage Goals

- ✅ All 7 Gherkin scenarios have corresponding test stubs
- ⬜ Implement fixture functions with sample data
- ⬜ Implement test logic with assertions
- ⬜ Add OpenAI API mocking
- ⬜ Add edge case tests
- ⬜ Achieve >90% code coverage
