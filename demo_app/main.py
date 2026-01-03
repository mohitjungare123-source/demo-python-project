"""Main application entry point"""

from demo_app import greet, add_numbers, multiply_numbers, is_prime, get_non_primes


def main():
    """Main function to demonstrate the application."""
    print("=" * 50)
    print("Welcome to Demo Python Project")
    print("=" * 50)
    print()

    # Test greet function
    print("Testing greet function:")
    message = greet("Alice")
    print(f"  {message}")
    print()

    # Test add_numbers function
    print("Testing add_numbers function:")
    result = add_numbers(10, 20)
    print(f"  10 + 20 = {result}")
    print()

    # Test multiply_numbers function
    print("Testing multiply_numbers function:")
    result = multiply_numbers(5, 6)
    print(f"  5 × 6 = {result}")
    print()

    # Test is_prime function
    print("Testing is_prime function:")
    test_numbers = [2, 9, 17, 20, 23]
    for num in test_numbers:
        prime_status = "prime" if is_prime(num) else "not prime"
        print(f"  {num} is {prime_status}")
    print()

    # Test get_non_primes function
    print("Testing get_non_primes function:")
    non_primes = get_non_primes(1, 20)
    print(f"  Non-prime numbers between 1 and 20: {non_primes}")
    print()

    print("=" * 50)
    print("Demo completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()

