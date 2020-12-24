# -*- coding: utf-8 -*-
from project_template import __version__


def main() -> None:
    """Print the current version of the project

    Examples
    --------
    >>> main()
    Project is version {}

    """.format(
        __version__
    )
    print(f"Project is version {__version__}")
