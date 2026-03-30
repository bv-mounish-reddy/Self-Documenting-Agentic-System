import math
import random

def calculate_area(shape, **kwargs):
    """
    Calculates the area of a given geometric shape.

    Args:
        shape (str): The type of shape ("circle" or "rectangle").
        **kwargs: Additional keyword arguments required for the shape's area calculation.
                  For "circle", expects 'radius'.
                  For "rectangle", expects 'width' and 'height'.

    Returns:
        float: The calculated area of the shape, or 0 if the shape is not recognized.
    """
    if shape == "circle":
        # Calculate area using the formula: pi * radius^2
        return math.pi * kwargs["radius"] ** 2
    elif shape == "rectangle":
        # Calculate area using the formula: width * height
        return kwargs["width"] * kwargs["height"]
    else:
        return 0

def divide_numbers(a, b):
    """
    Divides two numbers.

    Args:
        a (int or float): The numerator.
        b (int or float): The denominator.

    Returns:
        float: The result of the division.

    Raises:
        ZeroDivisionError: If the denominator 'b' is zero.
    """
    # Warning: This function does not handle ZeroDivisionError internally.
    # Ensure 'b' is not zero before calling to prevent runtime errors.
    return a / b

def process_list(items):
    """
    Processes a list of numbers by multiplying each item by 2 and summing the results.

    Args:
        items (list): A list of numbers (integers or floats).

    Returns:
        int or float: The total sum of all processed items.
    """
    total = 0  # Initialize total as an accumulator for the sum
    # Iterate through each item in the list
    for i in range(len(items)):
        # Multiply the current item by 2 and add it to the total
        total += items[i] * 2
    return total

class Calculator:
    """
    A simple calculator class that performs basic arithmetic operations
    and maintains a history of addition operations.
    """
    def __init__(self):
        """
        Initializes the Calculator with an empty history list.
        """
        self.history = []  # Stores a log of performed addition operations

    def add(self, a, b):
        """
        Adds two numbers and records the operation in the calculator's history.

        Args:
            a (int or float): The first number.
            b (int or float): The second number.

        Returns:
            int or float: The sum of 'a' and 'b'.
        """
        result = a + b
        # Record the addition operation and its result in the history
        self.history.append(f"{a} + {b} = {result}")
        return result

    def divide(self, a, b):
        """
        Divides two numbers by calling the external `divide_numbers` function.

        Args:
            a (int or float): The numerator.
            b (int or float): The denominator.

        Returns:
            float: The result of the division.

        Raises:
            ZeroDivisionError: If the denominator 'b' is zero (propagated from `divide_numbers`).
        """
        # Delegates the division task to the standalone divide_numbers function.
        # Warning: This method relies on `divide_numbers` and does not handle ZeroDivisionError itself.
        # The caller should ensure 'b' is not zero.
        return divide_numbers(a, b)

# Example Usage:
calc = Calculator()
result = calc.add(5, 3)
area = calculate_area("circle", radius=5)
division = calc.divide(10, 2)
items = [1, 2, 3, 4]
processed = process_list(items)
print(f"Results: {result}, {area:.2f}, {division}, {processed}")