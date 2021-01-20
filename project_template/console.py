# -*- coding: utf-8 -*-
"""Example module for best practices."""
from project_template import __version__


def main() -> None:
    """Print the current version of the project.

    Examples
    --------
    >>> main()
    Project is version 0.1.0

    """
    print(f"Project is version {__version__}")
