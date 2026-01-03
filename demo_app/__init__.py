"""Demo Python Application"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .utils import greet, add_numbers, multiply_numbers, is_prime, get_non_primes
from .desktop_cleaner import DesktopCleaner, organize_desktop, get_desktop_report

__all__ = [
    "greet",
    "add_numbers",
    "multiply_numbers",
    "is_prime",
    "get_non_primes",
    "DesktopCleaner",
    "organize_desktop",
    "get_desktop_report"
]

