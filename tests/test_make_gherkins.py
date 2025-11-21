"""
Test stubs for make_gherkins functionality.

Each test corresponds to one scenario in features/make_gherkins.feature.
Test docstrings are taken directly from the Gherkin scenarios.
"""

import pytest


from utils import make_gherkins, GherkinGenerator
from tests.conftest import FixtureError



# Fixtures
@pytest.fixture
def gherkin_generator(api_key, max_iterations, mock_openai_api):
    """
    Fixture to provide a GherkinGenerator instance with mocked OpenAI API.
    """
    try:
        return GherkinGenerator(api_key=api_key, max_iterations=max_iterations)
    except Exception as e:
        raise FixtureError(f"Failed to create GherkinGenerator fixture: {e}")


@pytest.fixture
def simple_function():
    """
    Fixture providing a simple function with a docstring containing description, parameters, and returns.
    """
    def add_numbers(a: int, b: int) -> int:
        """Add two numbers together.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            int: Sum of a and b
        """
        return a + b
    return add_numbers


@pytest.fixture
def function_with_multiple_parameters():
    """
    Fixture providing a callable with multiple documented parameters.
    """
    def process_data(name: str, age: int, email: str, active: bool) -> dict:
        """Process user data with multiple parameters.
        
        Args:
            name: User's full name
            age: User's age in years
            email: User's email address
            active: Whether user account is active
            
        Returns:
            dict: Processed user data
        """
        return {"name": name, "age": age, "email": email, "active": active}
    return process_data


@pytest.fixture
def function_with_examples():
    """
    Fixture providing a callable with docstring examples.
    """
    def multiply(x: int, y: int) -> int:
        """Multiply two numbers.
        
        Args:
            x: First number
            y: Second number
            
        Returns:
            int: Product of x and y
            
        Examples:
            multiply(2, 3)  # Returns 6
            multiply(5, 4)  # Returns 20
            multiply(0, 10) # Returns 0
        """
        return x * y
    return multiply


@pytest.fixture
def class_method_with_docstring():
    """
    Fixture providing a class method with a comprehensive docstring.
    """
    class Calculator:
        """A simple calculator class."""
        
        def __init__(self, precision: int = 2):
            """Initialize calculator.
            
            Args:
                precision: Decimal places for rounding
            """
            self.precision = precision
        
        def divide(self, a: float, b: float) -> float:
            """Divide two numbers with precision.
            
            Args:
                a: Numerator
                b: Denominator
                
            Returns:
                float: Result of division rounded to precision
                
            Raises:
                ZeroDivisionError: If b is zero
            """
            return round(a / b, self.precision)
    
    return Calculator().divide


@pytest.fixture
def callable_without_docstring():
    """
    Fixture providing a callable without a docstring.
    """
    def no_docs(x):
        return x * 2
    return no_docs


@pytest.fixture
def callable_with_complete_docstring():
    """
    Fixture providing a callable with a complete docstring.
    """
    def complete_function(data: list, threshold: int = 10) -> dict:
        """Process a list of data with comprehensive documentation.
        
        This function filters and processes data based on a threshold value.
        It returns a dictionary with statistics and filtered results.
        
        Args:
            data: List of integer values to process
            threshold: Minimum value to include (default: 10)
            
        Returns:
            dict: Dictionary containing:
                - count: Number of items above threshold
                - sum: Sum of filtered items
                - items: List of filtered items
                
        Raises:
            TypeError: If data is not a list
            ValueError: If threshold is negative
            
        Examples:
            complete_function([5, 15, 20], 10)  # Returns {'count': 2, 'sum': 35, 'items': [15, 20]}
            complete_function([1, 2, 3], 0)     # Returns {'count': 3, 'sum': 6, 'items': [1, 2, 3]}
        """
        if not isinstance(data, list):
            raise TypeError("data must be a list")
        if threshold < 0:
            raise ValueError("threshold must be non-negative")
        
        filtered = [x for x in data if x >= threshold]
        return {
            "count": len(filtered),
            "sum": sum(filtered),
            "items": filtered
        }
    return complete_function


@pytest.fixture
def function_dict(
    simple_function,
    function_with_multiple_parameters,
    function_with_examples,
    class_method_with
):
    return {
        "simple_function": simple_function,
        "function_with_multiple_parameters": function_with_multiple_parameters,
        "function_with_examples": function_with_examples,
        "class_method_with_docstring": class_method_with
    } 


@pytest.fixture
def mock_gherkin_content():
    """
    Fixture providing sample Gherkin content for validation tests.
    """
    return """Feature: Sample Feature
  As a user
  I want to use the function
  So that I can get results

  Background:
    Given the callable 'sample' with signature (x: int) -> int
    And the callable is accessible through the public API

  Scenario: Main execution
    Given an integer input
    When I call sample with the input
    Then it should return an integer result"""


@pytest.fixture
def mock_metadata():
    """
    Fixture providing sample metadata for validation tests.
    """
    return {
        "feature_name": "Sample Feature",
        "feature_file_path": "features/sample.feature",
        "creation_timestamp": "2025-11-19T03:00:00",
        "callable_name": "sample",
        "callable_signature": "(x: int) -> int",
        "num_scenarios": 2,
        "content_hash": "abc123def456",
        "has_examples": False,
        "has_parameters": True,
        "has_return": True,
        "content_length": 250,
        "description": "Sample function description",
        "llm_iterations": 3
    }



def test_generate_gherkin_from_simple_function_docstring__metadata_dictionary_returned(
    simple_function, api_key, mock_openai_api
):
    """
    Given a callable with a docstring containing description, parameters, and returns
    When I call make_gherkins with the callable's docstring
    Then a metadata dictionary should be returned
    """
    content, metadata = make_gherkins(simple_function, api_key=api_key)
    
    assert isinstance(metadata, dict), "make_gherkins should return a metadata dictionary"



def test_generate_gherkin_from_simple_function_docstring__gherkin_file_generated(
    simple_function, api_key, mock_openai_api
):
    """
    Given a callable with a docstring containing description, parameters, and returns
    When I call make_gherkins with the callable's docstring
    Then a Gherkin feature file should be generated
    """
    content, metadata = make_gherkins(simple_function, api_key=api_key)
    
    assert len(content) > 0, "Generated Gherkin content should not be empty"


def test_handle_callable_without_docstring__minimal_gherkin_generated(
    callable_without_docstring, api_key, mock_openai_api
):
    """
    Given a callable without a docstring
    When I call make_gherkins with the callable
    Then a minimal Gherkin feature file should be generated
    """
    content, metadata = make_gherkins(callable_without_docstring, api_key=api_key)
    
    assert len(content) > 0, "Even without docstring, a minimal Gherkin file should be generated"


@pytest.mark.parametrize("fixture_name", [
    "class_method_with_docstring",
    "function_with_examples",
    "function_with_multiple_parameters",
    "simple_function",
])
class TestGherkinContentSections:

    @pytest.mark.parametrize("fixture_name,expected_content", [
        "Background:",
        "Feature:",
        "Scenario:",
        "Examples:",
        "Scenario:",
        "API",
        "Given",
        "Scenario:",
        "When",
        "Then",
        "Background:",
        "Feature:",
        "Scenario:",
    ])
    def test_generate_gherkin_contains_expected_content(
        fixture_name, expected_content, request, api_key, mock_openai_api
    ):
        """
        Given a callable with a docstring
        When I call make_gherkins with the callable's docstring
        Then the generated content should contain the expected sections
        """
        callable_fixture = request.getfixturevalue(fixture_name)
        content, metadata = make_gherkins(callable_fixture, api_key=api_key)
        
        assert expected_content in content, \
            f"Gherkin did not contain the expected '{expected_content}' section\n{content}"

    @pytest.mark.parametrize("expected_field", [
        "creation_timestamp",
        "description",
        "has_examples",
        'callable_name',
        'callable_signature',
    ])
    def test_generate_gherkin_from_simple_function_docstring__metadata_contains_fields(
        expected_field, fixture_name, expected_content, request, api_key, mock_openai_api
    ):
        """
        Given a callable with a docstring containing description, parameters, and returns
        When I call make_gherkins with the callable's docstring
        Then the metadata dictionary should contain required fields
        """
        callable_fixture = request.getfixturevalue(fixture_name)
        content, metadata = make_gherkins(callable_fixture, api_key=api_key)

        assert expected_field in metadata, \
            f"Expected metatadata to contain field '{expected_field}', but it didn't\n{metadata}"


@pytest.mark.parametrize("field", [
    "feature_file_path",
    "feature_name",
    "creation_timestamp",
    "num_scenarios",
    "content_hash",
])
def test_return_comprehensive_metadata_dictionary_contains_required_fields(
    field, callable_with_complete_docstring, api_key, mock_openai_api
):
    """
    Given a callable with a complete docstring
    When I call make_gherkins with the callable's docstring
    Then the dictionary should contain the required metadata fields
    """
    content, metadata = make_gherkins(callable_with_complete_docstring, api_key=api_key)

    assert field in metadata, f"Metadata must containt '{field}' field, but it didn't"


@pytest.mark.parametrize("fixture_name,field,expected_value", [
    ("function_with_multiple_parameters", "has_parameters", True),
    ("function_with_multiple_parameters", "has_return", True),
    ("function_with_examples", "has_examples", True),
    ("callable_without_docstring", "has_parameters", False),
    ("callable_without_docstring", "has_return", False),
])
def test_metadata_boolean_fields(
    fixture_name, field, expected_value, request, api_key
):
    """
    Given an arbitrary callable
    When I call make_gherkins with that callable
    Then the metadata dictionary should reflect the presence of parameters, return values, and examples in the callable.
    """
    callable_fixture = request.getfixturevalue(fixture_name)
    _, metadata = make_gherkins(callable_fixture, api_key=api_key)

    assert metadata[field] is expected_value, f"Expected metadata field '{field}' to be '{expected_value}', but got '{metadata[field]}'"

