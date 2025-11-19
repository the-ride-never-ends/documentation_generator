"""
Pytest configuration and shared fixtures for make_gherkins tests.
"""

import pytest


@pytest.fixture(scope="session")
def mock_openai_api():
    """
    Mock OpenAI API for testing without making actual API calls.
    
    This fixture should be used to mock OpenAI responses in tests
    to avoid API costs and network dependencies.
    """
    pass


@pytest.fixture
def api_key():
    """
    Provide API key for testing.
    
    Can be mocked or read from environment variable.
    """
    pass


@pytest.fixture
def max_iterations():
    """
    Default max iterations for testing.
    """
    pass
