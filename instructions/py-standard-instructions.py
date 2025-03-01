# Python Code Standards

# 1. Formatting Rules
INDENTATION = "Use 4 spaces per indentation level. Do not use tabs."
MAX_LINE_LENGTH = "Limit all lines to a maximum of 79 characters."
BLANK_LINES = "Use two blank lines between top-level definitions (e.g., classes, functions). Use one blank line between methods inside a class."

# Example:
# Correct:
# def my_function():
#     pass
#
# def another_function():
#     pass

# Incorrect:
# def my_function():
#     pass
# def another_function():
#     pass

# 2. Naming Conventions
CLASS_NAMES = "Use PascalCase for class names (e.g., MyClass)."
FUNCTION_NAMES = "Use snake_case for function and method names (e.g., my_function)."
VARIABLE_NAMES = "Use snake_case for variable names (e.g., my_variable)."
CONSTANT_NAMES = "Use UPPERCASE with underscores for constant names (e.g., MY_CONSTANT)."
MODULE_NAMES = "Use lowercase and underscores for module filenames (e.g., my_module.py)."

# Example:
# Correct:
# class MyClass:
#     def my_function(self):
#         my_variable = 10
#         return my_variable

# Incorrect:
# class myclass:
#     def MyFunction(self):
#         MyVariable = 10
#         return MyVariable

# 3. Import Guidelines
IMPORTS_ORDER = "Group imports in the following order: standard library, third-party libraries, local application imports. Use a blank line between each group."
IMPORT_STYLE = "Avoid wildcard imports (e.g., from module import *). Use explicit imports instead."

# Example:
# Correct:
# import os
# import sys
#
# import numpy as np
#
# from my_module import my_function

# Incorrect:
# from my_module import *
# import numpy as np
# import os

# 4. Code Structure
FUNCTION_LENGTH = "Functions should ideally be no longer than 50 lines. Break down larger functions into smaller, reusable pieces."
COMMENT_STYLE = "Use comments to explain why the code exists, not what it does. Use complete sentences."
DOCSTRINGS = "Use docstrings for all public modules, classes, and functions. Follow the Google or NumPy docstring style."
EXCEPTION_HANDLING = "Catch specific exceptions instead of using a blanket 'except:'. Always log or handle exceptions appropriately."

# Example:
# Correct:
# def my_function(value: int) -> str:
#     """Returns a string representation of the value."""
#     if value < 0:
#         raise ValueError("Value cannot be negative.")
#     return str(value)

# Incorrect:
# def my_function(value: int) -> str:
#     # Convert value to string
#     if value < 0:
#         # Raise error if value is negative
#         raise ValueError("Value cannot be negative.")
#     return str(value)

# 5. Type Hints
TYPE_HINTS = "Use type hints for function arguments and return values (e.g., def my_function(name: str, age: int) -> bool)."

# Example:
# Correct:
# def my_function(name: str, age: int) -> bool:
#     return True

# Incorrect:
# def my_function(name, age):
#     return True

# 6. Code Readability
BOOLEAN_CHECKS = "Avoid comparisons to True, False, or None using equality operators. Use 'if variable' or 'if not variable' instead."
COMPREHENSIONS = "Use list comprehensions or generator expressions where appropriate, but avoid overly complex expressions."

# Example:
# Correct:
# if my_variable:
#     pass

# Incorrect:
# if my_variable == True:
#     pass

# 7. Testing Standards
UNIT_TESTS = "Write unit tests for all functions and methods. Use a framework like unittest or pytest."
TEST_NAMES = "Name test methods descriptively (e.g., test_function_returns_true)."

# Example:
# Correct:
# def test_function_returns_true():
#     assert my_function() is True

# Incorrect:
# def test_func():
#     assert my_function() is True

# Example Script that Aligns with Standards
from typing import List

class Calculator:
    """A simple calculator class to perform basic arithmetic operations."""

    def add(self, a: float, b: float) -> float:
        """Returns the sum of two numbers."""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Returns the difference between two numbers."""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Returns the product of two numbers."""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Returns the division of two numbers. Raises an error if dividing by zero."""
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b


def calculate_average(numbers: List[float]) -> float:
    """Calculates and returns the average of a list of numbers."""
    if not numbers:
        raise ValueError("The list of numbers cannot be empty.")
    return sum(numbers) / len(numbers)


if __name__ == "__main__":
    calc = Calculator()
    print("Addition: ", calc.add(10, 5))
    print("Subtraction: ", calc.subtract(10, 5))
    print("Multiplication: ", calc.multiply(10, 5))
    print("Division: ", calc.divide(10, 5))

    numbers = [10, 20, 30, 40, 50]
    print("Average: ", calculate_average(numbers))
