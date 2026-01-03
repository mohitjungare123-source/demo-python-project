"""Unit tests for utility functions"""

import pytest
from demo_app.utils import greet, add_numbers, multiply_numbers, is_prime, get_non_primes


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


class TestIsPrime:
    """Tests for the is_prime function."""

    def test_prime_numbers(self):
        """Test that prime numbers are correctly identified."""
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        for num in primes:
            assert is_prime(num), f"{num} should be prime"

    def test_non_prime_numbers(self):
        """Test that non-prime numbers are correctly identified."""
        non_primes = [0, 1, 4, 6, 8, 9, 10, 12, 14, 15]
        for num in non_primes:
            assert not is_prime(num), f"{num} should not be prime"

    def test_negative_numbers(self):
        """Test that negative numbers are not prime."""
        assert not is_prime(-5)
        assert not is_prime(-1)


class TestGetNonPrimes:
    """Tests for the get_non_primes function."""

    def test_get_non_primes_range(self):
        """Test getting non-primes in a range."""
        non_primes = get_non_primes(1, 10)
        expected = [1, 4, 6, 8, 9, 10]
        assert non_primes == expected

    def test_get_non_primes_small_range(self):
        """Test getting non-primes in a small range."""
        non_primes = get_non_primes(1, 5)
        expected = [1, 4]
        assert non_primes == expected

    def test_get_non_primes_empty_result(self):
        """Test when range contains only primes."""
        non_primes = get_non_primes(2, 3)
        expected = []
        assert non_primes == expected

    def test_get_non_primes_with_larger_range(self):
        """Test getting non-primes in a larger range."""
        non_primes = get_non_primes(1, 20)
        # 1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20
        assert 2 not in non_primes  # 2 is prime
        assert 3 not in non_primes  # 3 is prime
        assert 4 in non_primes      # 4 is not prime
        assert 9 in non_primes      # 9 is not prime
        assert len(non_primes) == 12


