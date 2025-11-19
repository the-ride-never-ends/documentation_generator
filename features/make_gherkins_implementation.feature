Feature: Make Gherkins
  As a user of the make_gherkins function
  I want to use it according to its public contract
  So that I can achieve the documented behavior

  # Generate a Gherkin feature file from a callable's docstring
  # This is a convenience function that creates a GherkinGenerator instance and calls its make_gherkins method
  # It provides a simple public API for generating Gherkin files from callable docstrings.

  Background:
    Given the callable 'make_gherkins' with signature (callable_obj: Callable, docstring: Optional[str] = None, output_path: Optional[str] = None) -> Tuple[str, Dict[str, Any]]
    And the callable is accessible through the public API

  Scenario: Execute make_gherkins with valid inputs
    Given the following parameters are provided:
      | callable_obj | The callable object (function, method, or class) to document |
      | docstring | Optional docstring to use instead of extracting from callable |
      | output_path | Optional path where the feature file should be written |
    When I call make_gherkins with the provided parameters
    Then the function should return Tuple containing: - str: The generated Gherkin feature file content - Dict[str, Any]: Metadata dictionary with information about the generation
    And all behavior should conform to the public contract

  Scenario: Handle error conditions in make_gherkins
    Given invalid or edge case inputs are provided
    When I call make_gherkins with invalid parameters
    Then appropriate exceptions should be raised:
      # ValueError: If callable_obj is not a valid callable
    And the error messages should be descriptive

  Scenario Outline: Test make_gherkins with example inputs
    Given the following example inputs: <inputs>
    When I execute make_gherkins
    Then I should get the expected result: <output>

    Examples:
      | inputs | output |
      | >>> def example_function(x: int) -> int: | expected |
      | ...     '''Multiply x by 2. | expected |
      | ... | expected |
      | ...     Args: | expected |
      | ...         x: Input number | expected |
      | ... | expected |
      | ...     Returns: | expected |
      | ...         int: Result of x * 2 | expected |
      | ...     ''' | expected |
      | ...     return x * 2 | expected |
      | >>> content, metadata = make_gherkins(ex | expected |
      | >>> assert 'Feature:' in content | expected |
      | >>> assert metadata['callable_name'] ==  | expected |

  Scenario: Verify make_gherkins public contract
    Given the make_gherkins callable is part of the public API
    When I inspect its interface
    Then all documented features should be accessible
    And the behavior should match the documentation
    And no internal implementation details should be exposed