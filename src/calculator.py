"""
Core calculator logic. Pure functions, no I/O, no FastAPI imports here.
Keeping this layer framework-agnostic makes it trivially unit-testable
(same idea as keeping business logic out of your route handlers in v8-aig-router).
"""

from typing import Union

Number = Union[int, float]


def _validate_numeric(*values: object) -> None:
    for v in values:
        if not isinstance(v, (int, float)):
            raise TypeError(f"Arguments must be numeric, got {type(v).__name__}")


def add(a: Number, b: Number) -> Number:
    _validate_numeric(a, b)
    return a + b


def subtract(a: Number, b: Number) -> Number:
    _validate_numeric(a, b)
    return a - b


def multiply(a: Number, b: Number) -> Number:
    _validate_numeric(a, b)
    return a * b


def divide(a: Number, b: Number) -> Number:
    _validate_numeric(a, b)
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


OPERATIONS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
}
