# Tests for make_gherkins

This directory contains test stubs for the `make_gherkins` functionality.

## Structure

- **`test_make_gherkins.py`** - Test stubs mapping one-to-one with Gherkin scenarios
- **`conftest.py`** - Pytest configuration and shared fixtures
- **`__init__.py`** - Package initialization

## Test Design

Each test stub follows the **atomic test principle**: one Given, one When, one Then (no And clauses).

The original 7 Gherkin scenarios have been split into **29 focused test stubs** where each "And" clause from the original scenarios becomes its own test.

### Test Naming Convention

Tests are named to indicate which scenario they belong to and what specific assertion they test:

```
test_<scenario_name>__<specific_assertion>
```

### Test Docstrings

Test docstrings contain only **one Given-When-Then clause** (no And):

```python
def test_generate_gherkin_from_simple_function_docstring__gherkin_file_generated(simple_function):
    """
    Given a callable with a docstring containing description, parameters, and returns
    When I call make_gherkins with the callable's docstring
    Then a Gherkin feature file should be generated
    """
    pass


def test_generate_gherkin_from_simple_function_docstring__feature_section_with_description(simple_function):
    """
    Given a callable with a docstring containing description, parameters, and returns
    When I call make_gherkins with the callable's docstring
    Then the feature file should contain a Feature section with the description
    """
    pass
```

### Test Organization

- **Scenario 1**: 6 tests (one Then + 5 Ands split)
- **Scenario 2**: 4 tests (one Then + 3 Ands split)
- **Scenario 3**: 3 tests (one Then + 2 Ands split)
- **Scenario 4**: 3 tests (one Then + 2 Ands split)
- **Scenario 5**: 3 tests (one Then + 2 Ands split)
- **Scenario 6**: 4 tests (one Then + 3 Ands split)
- **Scenario 7**: 6 tests (one Then + 5 Ands split)

**Total**: 29 atomic test stubs

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

Each test should focus on **one specific assertion**:

```python
def test_generate_gherkin_from_simple_function_docstring__gherkin_file_generated(simple_function, api_key):
    """
    Given a callable with a docstring containing description, parameters, and returns
    When I call make_gherkins with the callable's docstring
    Then a Gherkin feature file should be generated
    """
    # When
    content, metadata = make_gherkins(simple_function, api_key=api_key)
    
    # Then - Single focused assertion
    assert 'Feature:' in content
    assert len(content) > 0


def test_generate_gherkin_from_simple_function_docstring__metadata_contains_timestamp(simple_function, api_key):
    """
    Given a callable with a docstring containing description, parameters, and returns
    When I call make_gherkins with the callable's docstring
    Then the metadata dictionary should contain creation timestamp
    """
    # When
    content, metadata = make_gherkins(simple_function, api_key=api_key)
    
    # Then - Single focused assertion
    assert 'creation_timestamp' in metadata
    assert metadata['creation_timestamp'] is not None
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

- ✅ All 7 Gherkin scenarios split into 29 atomic test stubs
- ✅ Each test follows one Given-When-Then pattern (no And clauses)
- ⬜ Implement fixture functions with sample data
- ⬜ Implement test logic with focused assertions
- ⬜ Add OpenAI API mocking
- ⬜ Add edge case tests
- ⬜ Achieve >90% code coverage

## Benefits of Atomic Tests

**Focused Testing**: Each test validates one specific behavior  
**Easier Debugging**: Failed tests immediately identify the problem  
**Better Isolation**: Tests don't have cascading failures  
**Clearer Intent**: Test names describe exactly what's being tested  
**Independent Execution**: Tests can run in any order
