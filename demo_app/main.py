"""Main application entry point"""

from demo_app import greet, add_numbers, multiply_numbers


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

    print("=" * 50)
    print("Demo completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()

