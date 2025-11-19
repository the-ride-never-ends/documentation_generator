"""
Documentation Generator Package.

This package provides tools for parsing Python code and generating documentation.
"""

from .gherkin_generator import make_gherkins, GherkinGenerator

__version__ = "0.1.0"
__all__ = ['make_gherkins', 'GherkinGenerator']