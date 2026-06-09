"""Sample module used by the analyzer unit tests. Do not edit casually —
the tests assert on the exact symbols defined here.
"""

CONST = 42


def greet(name):
    """Return a greeting."""
    return f"hello {name}"


class Animal:
    """A test class with two methods."""

    def speak(self):
        return "..."

    def legs(self):
        return 4
