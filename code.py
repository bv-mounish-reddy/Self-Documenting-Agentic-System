import math
import random # The 'random' module is imported but not used in this script.

def calculate_area(shape, **kwargs):
    """
    Calculates the area of various geometric shapes.

    Args:
        shape (str): The type of the shape (e.g., "circle", "rectangle").
        **kwargs: Additional keyword arguments specific to the shape:
                  - For "circle": 'radius' (float or int)
                  - For "rectangle": 'width' (float or int), 'height' (float or int)

    Returns:
        float: The calculated area of the shape. Returns 0 if the shape is unknown.

    Raises:
        KeyError: If required keyword arguments (e.g., 'radius' for circle,
                  'width' or 'height' for rectangle) are missing for the specified shape.
    """
    if shape == "circle":
        # Calculate area of a circle using the formula: pi * radius^2
        # Warning: This will raise a KeyError if 'radius' is not provided in kwargs.
        return math.pi * kwargs["radius"] ** 2
    elif shape == "rectangle":
        # Calculate area of a rectangle using the formula: width * height
        # Warning: This will raise a KeyError if 'width' or 'height' is not provided in kwargs.
        return kwargs["width"] * kwargs["height"]
    else:
        # Warning: Returns 0 for unknown shapes.
        # Consider raising an error or returning None for better error handling
        # when an unsupported shape is requested.
        return 0

def divide_numbers(a, b):
    """
    Divides two numbers.

    Args:
        a (float or int): The numerator.
        b (float or int): The denominator.

    Returns:
        float: The result of the division.

    Raises:
        ZeroDivisionError: If the denominator 'b' is zero.
        # Note: The original code does not explicitly handle ZeroDivisionError,
        # it will raise a runtime error if 'b' is 0.
    """
    # Warning: This function will raise a ZeroDivisionError if 'b' is 0.
    # For robust applications, consider adding a try-except block or a check for b == 0.
    return a / b

def process_list(items):
    """
    Processes a list of numbers by multiplying each item by 2 and summing the results.

    Args:
        items (list): A list of numbers (integers or floats).

    Returns:
        float or int: The total sum of the processed items.
    """
    total = 0 # Initialize the accumulator for the sum
    # Iterate through the list using an index
    for i in range(len(items)):
        # Multiply each item by 2 and add it to the running total
        total += items[i] * 2
    return total

class Calculator:
    """
    A simple calculator class that performs basic arithmetic operations
    and keeps a history of addition operations.
    """
    def __init__(self):
        """
        Initializes the Calculator with an empty history list.
        """
        self.history = [] # Stores a log of performed addition operations

    def add(self, a, b):
        """
        Adds two numbers and records the operation in the calculator's history.

        Args:
            a (float or int): The first number.
            b (float or int): The second number.

        Returns:
            float or int: The sum of 'a' and 'b'.
        """
        result = a + b # Perform the addition operation
        # Append a formatted string of the operation and its result to the history
        self.history.append(f"{a} + {b} = {result}")
        return result

    def divide(self, a, b):
        """
        Divides two numbers by calling the external 'divide_numbers' function.

        Args:
            a (float or int): The numerator.
            b (float or int): The denominator.

        Returns:
            float: The result of the division.

        Raises:
            ZeroDivisionError: If the denominator 'b' is zero (propagated from divide_numbers).
        """
        # Delegates the division operation to the standalone divide_numbers function.
        # This method inherits the potential ZeroDivisionError from divide_numbers.
        return divide_numbers(a, b)

# --- Example Usage ---

# Create an instance of the Calculator class
calc = Calculator()

# Perform an addition operation using the calculator instance
result = calc.add(5, 3)

# Calculate the area of a circle using the standalone function
# The radius is passed as a keyword argument
area = calculate_area("circle", radius=5)

# Perform a division operation using the calculator's method
division = calc.divide(10, 2)

# Define a list of numbers to be processed
items = [1, 2, 3, 4]

# Process the list using the standalone process_list function
processed = process_list(items)

# Print all the calculated results to the console
# The 'area' is formatted to two decimal places for readability
print(f"Results: {result}, {area:.2f}, {division}, {processed}")