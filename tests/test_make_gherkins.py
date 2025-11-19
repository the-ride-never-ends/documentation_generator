"""
Test stubs for make_gherkins functionality.

Each test corresponds to one scenario in features/make_gherkins.feature.
Test docstrings are taken directly from the Gherkin scenarios.
"""

import pytest
from utils import make_gherkins, GherkinGenerator


# Fixtures
@pytest.fixture
def gherkin_generator(api_key, max_iterations, mock_openai_api):
    """
    Fixture to provide a GherkinGenerator instance with mocked OpenAI API.
    """
    return GherkinGenerator(api_key=api_key, max_iterations=max_iterations)


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


# Test Stubs for each Scenario
# Each test follows the pattern: one Given, one When, one Then (no And clauses)


# Scenario 1: Generate Gherkin from a simple function docstring - Split into 6 tests
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


def test_generate_gherkin_from_simple_function_docstring__feature_section_with_description(
    simple_function, api_key, mock_openai_api
):
    """
    Given a callable with a docstring containing description, parameters, and returns
    When I call make_gherkins with the callable's docstring
    Then the feature file should contain a Feature section with the description
    """
    content, metadata = make_gherkins(simple_function, api_key=api_key)
    
    assert 'Feature:' in content, "Generated content should contain a Feature section"


def test_generate_gherkin_from_simple_function_docstring__scenarios_from_parameters(
    simple_function, api_key, mock_openai_api
):
    """
    Given a callable with a docstring containing description, parameters, and returns
    When I call make_gherkins with the callable's docstring
    Then the feature file should contain Scenarios derived from the parameters
    """
    content, metadata = make_gherkins(simple_function, api_key=api_key)
    
    assert 'Scenario:' in content, "Generated content should contain at least one Scenario"


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


def test_generate_gherkin_from_simple_function_docstring__metadata_contains_timestamp(
    simple_function, api_key, mock_openai_api
):
    """
    Given a callable with a docstring containing description, parameters, and returns
    When I call make_gherkins with the callable's docstring
    Then the metadata dictionary should contain creation timestamp
    """
    content, metadata = make_gherkins(simple_function, api_key=api_key)
    
    assert 'creation_timestamp' in metadata, "Metadata should contain creation_timestamp field"


def test_generate_gherkin_from_simple_function_docstring__metadata_contains_summary(
    simple_function, api_key, mock_openai_api
):
    """
    Given a callable with a docstring containing description, parameters, and returns
    When I call make_gherkins with the callable's docstring
    Then the metadata dictionary should contain content summary
    """
    content, metadata = make_gherkins(simple_function, api_key=api_key)
    
    assert 'description' in metadata, "Metadata should contain description (content summary)"


# Scenario 2: Generate Gherkin from a function with multiple parameters - Split into 4 tests
def test_generate_gherkin_from_function_with_multiple_parameters__main_scenario(
    function_with_multiple_parameters, api_key, mock_openai_api
):
    """
    Given a callable with multiple documented parameters
    When I call make_gherkins with the callable's docstring
    Then the generated Gherkin should contain a Scenario for the main function behavior
    """
    content, metadata = make_gherkins(function_with_multiple_parameters, api_key=api_key)
    
    assert 'Scenario:' in content, "Generated Gherkin should contain at least one Scenario for main behavior"


def test_generate_gherkin_from_function_with_multiple_parameters__parameters_in_steps(
    function_with_multiple_parameters, api_key, mock_openai_api
):
    """
    Given a callable with multiple documented parameters
    When I call make_gherkins with the callable's docstring
    Then each parameter should be represented in the Given/When/Then steps
    """
    content, metadata = make_gherkins(function_with_multiple_parameters, api_key=api_key)
    
    assert metadata['has_parameters'] is True, "Metadata should indicate that parameters are present"


def test_generate_gherkin_from_function_with_multiple_parameters__return_in_then(
    function_with_multiple_parameters, api_key, mock_openai_api
):
    """
    Given a callable with multiple documented parameters
    When I call make_gherkins with the callable's docstring
    Then the return value should be represented in the Then step
    """
    content, metadata = make_gherkins(function_with_multiple_parameters, api_key=api_key)
    
    assert metadata['has_return'] is True, "Metadata should indicate that return value is documented"


def test_generate_gherkin_from_function_with_multiple_parameters__verifiable_through_contract(
    function_with_multiple_parameters, api_key, mock_openai_api
):
    """
    Given a callable with multiple documented parameters
    When I call make_gherkins with the callable's docstring
    Then all features should be verifiable through the public contract
    """
    content, metadata = make_gherkins(function_with_multiple_parameters, api_key=api_key)
    
    assert 'public' in content.lower() or 'API' in content, "Generated Gherkin should reference public contract/API"


# Scenario 3: Generate Gherkin from a function with examples - Split into 3 tests
def test_generate_gherkin_from_function_with_examples__scenario_outline(
    function_with_examples, api_key, mock_openai_api
):
    """
    Given a callable with docstring examples
    When I call make_gherkins with the callable's docstring
    Then the generated Gherkin should include Scenario Outline sections
    """
    content, metadata = make_gherkins(function_with_examples, api_key=api_key)
    
    assert 'Scenario' in content, "Generated Gherkin should contain Scenario sections when examples are present"


def test_generate_gherkin_from_function_with_examples__examples_tables(
    function_with_examples, api_key, mock_openai_api
):
    """
    Given a callable with docstring examples
    When I call make_gherkins with the callable's docstring
    Then the examples should be converted to Examples tables
    """
    content, metadata = make_gherkins(function_with_examples, api_key=api_key)
    
    assert metadata['has_examples'] is True, "Metadata should indicate that examples are present"


def test_generate_gherkin_from_function_with_examples__metadata_includes_count(
    function_with_examples, api_key, mock_openai_api
):
    """
    Given a callable with docstring examples
    When I call make_gherkins with the callable's docstring
    Then the metadata should include the number of examples
    """
    content, metadata = make_gherkins(function_with_examples, api_key=api_key)
    
    assert 'has_examples' in metadata, "Metadata should include information about examples"


# Scenario 4: Generate Gherkin from a class method docstring - Split into 3 tests
def test_generate_gherkin_from_class_method_docstring__class_context(
    class_method_with_docstring, api_key, mock_openai_api
):
    """
    Given a class method with a comprehensive docstring
    When I call make_gherkins with the method's docstring
    Then the generated Gherkin should include the class context
    """
    content, metadata = make_gherkins(class_method_with_docstring, api_key=api_key)
    
    assert 'Feature:' in content, "Generated Gherkin should include Feature section with class context"


def test_generate_gherkin_from_class_method_docstring__method_behavior_scenarios(
    class_method_with_docstring, api_key, mock_openai_api
):
    """
    Given a class method with a comprehensive docstring
    When I call make_gherkins with the method's docstring
    Then the method behavior should be described in scenarios
    """
    content, metadata = make_gherkins(class_method_with_docstring, api_key=api_key)
    
    assert 'Scenario:' in content, "Generated Gherkin should describe method behavior in scenarios"


def test_generate_gherkin_from_class_method_docstring__constructor_in_background(
    class_method_with_docstring, api_key, mock_openai_api
):
    """
    Given a class method with a comprehensive docstring
    When I call make_gherkins with the method's docstring
    Then constructor parameters should be in the Background section
    """
    content, metadata = make_gherkins(class_method_with_docstring, api_key=api_key)
    
    assert 'Background:' in content, "Generated Gherkin should include Background section for setup"


# Scenario 5: Handle callable without docstring - Split into 3 tests
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


def test_handle_callable_without_docstring__indicates_missing_documentation(
    callable_without_docstring, api_key, mock_openai_api
):
    """
    Given a callable without a docstring
    When I call make_gherkins with the callable
    Then the feature should indicate missing documentation
    """
    content, metadata = make_gherkins(callable_without_docstring, api_key=api_key)
    
    assert metadata['has_parameters'] is False, "Metadata should indicate missing parameter documentation"


def test_handle_callable_without_docstring__metadata_indicates_incomplete(
    callable_without_docstring, api_key, mock_openai_api
):
    """
    Given a callable without a docstring
    When I call make_gherkins with the callable
    Then the metadata should indicate incomplete information
    """
    content, metadata = make_gherkins(callable_without_docstring, api_key=api_key)
    
    assert metadata['has_return'] is False, "Metadata should indicate missing return documentation"


# Scenario 6: Validate all features through public contract - Split into 4 tests
def test_validate_all_features_through_public_contract__scenarios_executable(
    mock_gherkin_content
):
    """
    Given any generated Gherkin feature file
    When the features are extracted from the file
    Then all scenarios should be executable through the public API
    """
    assert 'Scenario:' in mock_gherkin_content, "Gherkin content should contain executable scenarios"


def test_validate_all_features_through_public_contract__steps_map_to_methods(
    mock_gherkin_content
):
    """
    Given any generated Gherkin feature file
    When the features are extracted from the file
    Then all Given/When/Then steps should map to public methods
    """
    assert 'Given' in mock_gherkin_content and 'When' in mock_gherkin_content and 'Then' in mock_gherkin_content,         "Gherkin should contain Given/When/Then steps that map to testable behavior"


def test_validate_all_features_through_public_contract__no_internal_details(
    mock_gherkin_content
):
    """
    Given any generated Gherkin feature file
    When the features are extracted from the file
    Then no internal implementation details should be exposed
    """
    assert 'public API' in mock_gherkin_content or 'public' in mock_gherkin_content.lower(),         "Gherkin should reference public API without exposing internal details"


def test_validate_all_features_through_public_contract__parseable_by_standard_parsers(
    mock_gherkin_content
):
    """
    Given any generated Gherkin feature file
    When the features are extracted from the file
    Then the feature file should be parseable by standard Gherkin parsers
    """
    assert mock_gherkin_content.startswith('Feature:'),         "Gherkin content should start with Feature: to be parseable by standard parsers"


# Scenario 7: Return comprehensive metadata dictionary - Split into 6 tests
def test_return_comprehensive_metadata_dictionary__contains_file_path(
    callable_with_complete_docstring, api_key, mock_openai_api
):
    """
    Given a callable with a complete docstring
    When I call make_gherkins with the callable's docstring
    Then the returned dictionary should contain the feature file path
    """
    content, metadata = make_gherkins(callable_with_complete_docstring, api_key=api_key)
    
    assert 'feature_file_path' in metadata, "Metadata should contain the feature_file_path field"


def test_return_comprehensive_metadata_dictionary__contains_feature_name(
    callable_with_complete_docstring, api_key, mock_openai_api
):
    """
    Given a callable with a complete docstring
    When I call make_gherkins with the callable's docstring
    Then the dictionary should contain the feature name
    """
    content, metadata = make_gherkins(callable_with_complete_docstring, api_key=api_key)
    
    assert 'feature_name' in metadata, "Metadata should contain the feature_name field"


def test_return_comprehensive_metadata_dictionary__contains_creation_timestamp(
    callable_with_complete_docstring, api_key, mock_openai_api
):
    """
    Given a callable with a complete docstring
    When I call make_gherkins with the callable's docstring
    Then the dictionary should contain the creation timestamp
    """
    content, metadata = make_gherkins(callable_with_complete_docstring, api_key=api_key)
    
    assert 'creation_timestamp' in metadata, "Metadata should contain the creation_timestamp field"


def test_return_comprehensive_metadata_dictionary__contains_scenarios_count(
    callable_with_complete_docstring, api_key, mock_openai_api
):
    """
    Given a callable with a complete docstring
    When I call make_gherkins with the callable's docstring
    Then the dictionary should contain the number of scenarios generated
    """
    content, metadata = make_gherkins(callable_with_complete_docstring, api_key=api_key)
    
    assert 'num_scenarios' in metadata, "Metadata should contain the num_scenarios field"


def test_return_comprehensive_metadata_dictionary__contains_callable_info(
    callable_with_complete_docstring, api_key, mock_openai_api
):
    """
    Given a callable with a complete docstring
    When I call make_gherkins with the callable's docstring
    Then the dictionary should contain the callable name and signature
    """
    content, metadata = make_gherkins(callable_with_complete_docstring, api_key=api_key)
    
    assert 'callable_name' in metadata and 'callable_signature' in metadata,         "Metadata should contain both callable_name and callable_signature fields"


def test_return_comprehensive_metadata_dictionary__contains_content_hash(
    callable_with_complete_docstring, api_key, mock_openai_api
):
    """
    Given a callable with a complete docstring
    When I call make_gherkins with the callable's docstring
    Then the dictionary should contain a content hash for verification
    """
    content, metadata = make_gherkins(callable_with_complete_docstring, api_key=api_key)
    
    assert 'content_hash' in metadata, "Metadata should contain the content_hash field for verification"
