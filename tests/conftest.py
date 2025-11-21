"""
Pytest configuration and shared fixtures for make_gherkins tests.
"""

import pytest
from unittest.mock import Mock, patch


class FixtureError(RuntimeError):
    """Custom exception for fixture-related errors."""
    pass


@pytest.fixture(scope="session")
def mock_openai_api():
    """
    Mock OpenAI API for testing without making actual API calls.
    
    This fixture should be used to mock OpenAI responses in tests
    to avoid API costs and network dependencies.
    """
    with patch('utils.gherkin_generator.OpenAI') as mock_openai:
        # Create mock response for chat completions
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = """Feature: Test Feature
  As a user
  I want to test
  So that it works

  Background:
    Given the callable 'test' with signature ()
    And the callable is accessible through the public API

  Scenario: Test scenario
    Given test inputs
    When I call test
    Then it should return a dictionary with keys: status, data"""
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        yield mock_openai


@pytest.fixture
def api_key():
    """
    Provide API key for testing.
    
    Returns a test API key for mocked OpenAI calls.
    """
    return "test-api-key-12345"


@pytest.fixture
def max_iterations():
    """
    Default max iterations for testing.
    """
    return 3
