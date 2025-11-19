Feature: Generate Gherkin Feature Files from Callable Docstrings
  As a developer using the documentation generator
  I want to convert callable docstrings into Gherkin feature files
  So that I can generate behavior-driven documentation from code

  Background:
    Given a documentation generator system with make_gherkins functionality
    And the system can parse docstrings in various formats

  Scenario: Generate Gherkin from a simple function docstring
    Given a callable with a docstring containing description, parameters, and returns
    When I call make_gherkins with the callable's docstring
    Then a Gherkin feature file should be generated
    And the feature file should contain a Feature section with the description
    And the feature file should contain Scenarios derived from the parameters
    And a metadata dictionary should be returned
    And the metadata dictionary should contain creation timestamp
    And the metadata dictionary should contain content summary

  Scenario: Generate Gherkin from a function with multiple parameters
    Given a callable with multiple documented parameters
    When I call make_gherkins with the callable's docstring
    Then the generated Gherkin should contain a Scenario for the main function behavior
    And each parameter should be represented in the Given/When/Then steps
    And the return value should be represented in the Then step
    And all features should be verifiable through the public contract

  Scenario: Generate Gherkin from a function with examples
    Given a callable with docstring examples
    When I call make_gherkins with the callable's docstring
    Then the generated Gherkin should include Scenario Outline sections
    And the examples should be converted to Examples tables
    And the metadata should include the number of examples

  Scenario: Generate Gherkin from a class method docstring
    Given a class method with a comprehensive docstring
    When I call make_gherkins with the method's docstring
    Then the generated Gherkin should include the class context
    And the method behavior should be described in scenarios
    And constructor parameters should be in the Background section

  Scenario: Handle callable without docstring
    Given a callable without a docstring
    When I call make_gherkins with the callable
    Then a minimal Gherkin feature file should be generated
    And the feature should indicate missing documentation
    And the metadata should indicate incomplete information

  Scenario: Validate all features through public contract
    Given any generated Gherkin feature file
    When the features are extracted from the file
    Then all scenarios should be executable through the public API
    And all Given/When/Then steps should map to public methods
    And no internal implementation details should be exposed
    And the feature file should be parseable by standard Gherkin parsers

  Scenario: Return comprehensive metadata dictionary
    Given a callable with a complete docstring
    When I call make_gherkins with the callable's docstring
    Then the returned dictionary should contain the feature file path
    And the dictionary should contain the feature name
    And the dictionary should contain the creation timestamp
    And the dictionary should contain the number of scenarios generated
    And the dictionary should contain the callable name and signature
    And the dictionary should contain a content hash for verification
