"""Unit tests for utility functions"""

import pytest
from demo_app.utils import greet, add_numbers, multiply_numbers


class TestGreet:
    """Tests for the greet function."""

    def test_greet_with_name(self):
        """Test greeting with a name."""
        result = greet("Bob")
        assert "Bob" in result
        assert "Hello" in result

    def test_greet_returns_string(self):
        """Test that greet returns a string."""
        result = greet("Alice")
        assert isinstance(result, str)


class TestAddNumbers:
    """Tests for the add_numbers function."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert add_numbers(2, 3) == 5

    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        assert add_numbers(-5, -3) == -8

    def test_add_zero(self):
        """Test adding with zero."""
        assert add_numbers(10, 0) == 10

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        assert add_numbers(10, -5) == 5


class TestMultiplyNumbers:
    """Tests for the multiply_numbers function."""

    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers."""
        assert multiply_numbers(3, 4) == 12

    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        assert multiply_numbers(5, 0) == 0

    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        assert multiply_numbers(-2, -3) == 6

    def test_multiply_mixed_numbers(self):
        """Test multiplying positive and negative numbers."""
        assert multiply_numbers(4, -2) == -8

