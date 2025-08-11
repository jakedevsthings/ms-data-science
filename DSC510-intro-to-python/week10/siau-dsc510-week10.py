"""
Siau, Jacob

DSC510-T303 Week 10 Assignment 10.1

Description:
    This script implements a simple cash register program. The program
    allows a user to add item prices until they choose to quit, then prints
    the total item count and total amount due formatted as currency.
"""

import locale


class CashRegister:
    """
    Simple cash register that tracks total price and item count.

    The register maintains a running total of prices and the number of items
    added. It provides methods to add a new item and to retrieve the total
    price and item count.

    Attributes:
        total_price: Running total of prices added to the register.
        item_count: Number of items added to the register.
    """

    def __init__(self):
        """Initialize a new, empty cash register."""
        self.total_price = 0.0
        self.item_count = 0

    def add_item(self, price):
        """
        Add a single item to the register.

        Args:
            price: The price of the item to add. Must be greater than 0.

        Raises:
            ValueError: If the provided price is not greater than 0.
        """
        if price <= 0:
            raise ValueError("Price must be greater than 0.")
        self.total_price += float(price)
        self.item_count += 1

    def get_total(self):
        """Return the running total price."""
        return self.total_price

    def get_count(self):
        """Return the total number of items added."""
        return self.item_count


def _configure_locale():
    """
    Configure a usable locale for currency formatting.

    Tries the system default first, then common fallbacks. Returns the name
    of the locale that was successfully set, or None if all attempts failed.
    """
    candidate_locales = [
        "",  # System default
        "en_US.UTF-8",  # Common on Unix-like systems
        "English_United States.1252",  # Common on Windows
    ]
    for loc in candidate_locales:
        try:
            locale.setlocale(locale.LC_ALL, loc)
            locale.currency(0.0, grouping=True)
            return locale.setlocale(locale.LC_ALL)
        except Exception:
            continue
    return None


def _format_currency(value):
    """
    Format a number as currency using the active locale.
    Falls back to a simple USD-style format if locale-based formatting fails.

    Args:
        value: The number to format as currency.

    Returns:
        The formatted currency string.
    """
    try:
        return locale.currency(value, grouping=True)
    except Exception:
        return f"${value:,.2f}"


def main():
    """
    Program entry point for the cash register application.
    """
    print("Welcome to the Cash Register Program!")

    set_loc = _configure_locale()
    if set_loc is None:
        print("Note: Could not configure system locale; using fallback currency formatting.")

    register = CashRegister()

    while True:
        user_input = input("Enter the item's price (or 'q' to checkout): ").strip()
        if user_input.lower() in {"q", "quit", "exit"}:
            break

        try:
            price = float(user_input)
        except ValueError:
            print("Invalid input. Please enter a numeric price or 'q' to checkout.")
            continue

        if price <= 0:
            print("Price must be greater than 0. Please try again.")
            continue

        try:
            register.add_item(price)
        except ValueError as exc:
            print(f"Error: {exc}")
            continue

        print(f"Added item #{register.get_count()}: {_format_currency(price)}")

    print("\nCheckout summary:")
    print(f"Total items: {register.get_count()}")
    print(f"Total amount: {_format_currency(register.get_total())}")
    print("Thank you for using the Cash Register Program!")


if __name__ == "__main__":
    main()
