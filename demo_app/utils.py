"""Utility functions for the demo application"""


def greet(name: str) -> str:
    """
    Greet a person by name.

    Args:
        name: The name of the person to greet

    Returns:
        A greeting message
    """
    return f"Hello, {name}! Welcome to the Demo Python Project."


def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b
    """
    return a + b


def multiply_numbers(a: int, b: int) -> int:
    """
    Multiply two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        The product of a and b
    """
    return a * b


def is_prime(num: int) -> bool:
    """
    Check if a number is prime.

    Args:
        num: The number to check

    Returns:
        True if the number is prime, False otherwise
    """
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(num ** 0.5) + 1, 2):
        if num % i == 0:
            return False
    return True


def get_non_primes(start: int, end: int) -> list:
    """
    Fetch all non-prime numbers in a given range.

    Args:
        start: The start of the range (inclusive)
        end: The end of the range (inclusive)

    Returns:
        A list of non-prime numbers in the range
    """
    non_primes = [num for num in range(start, end + 1) if not is_prime(num)]
    return non_primes


