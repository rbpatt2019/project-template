# -*- coding: utf-8 -*-
"""Nox session configuration."""
import tempfile
from typing import Any, List

import nox
from nox.sessions import Session

PACKAGE: str = "project_template"
LOCATIONS: List[str] = [
    PACKAGE,
    "noxfile.py",
    "tests",
]
VERSIONS: List[str] = ["3.9", "3.8", "3.7"]

nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = True


def constrained_install(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages with poetry version constraint."""
    with tempfile.NamedTemporaryFile() as reqs:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={reqs.name}",
            external=True,
        )
        session.install(f"--constraint={reqs.name}", *args, **kwargs)


@nox.session(python="3.9")
def form(session: Session) -> None:
    """Format code with isort and black."""
    args = session.posargs or LOCATIONS
    constrained_install(session, "isort", "black")
    session.run("isort", *args)
    session.run("black", *args)


@nox.session(python=VERSIONS)
def lint(session: Session) -> None:
    """Lint files with flake8."""
    args = session.posargs or LOCATIONS[:2]
    constrained_install(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-bugbear",
        "flake8-comprehensions",
        "flake8-docstrings",
        "flake8-pytest-style",
        "flake8-spellcheck",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python=VERSIONS)
def type(session: Session) -> None:
    """Type check files with mypy."""
    args = session.posargs or LOCATIONS
    constrained_install(session, "mypy")
    session.run("mypy", "--ignore-missing-imports", *args)


@nox.session(python=VERSIONS)
def security(session: Session) -> None:
    """Check security safety."""
    constrained_install(session, "safety")
    with tempfile.NamedTemporaryFile() as reqs:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={reqs.name}",
            external=True,
        )
        session.run("safety", "check", f"--file={reqs.name}", "--full-report")


@nox.session(python=VERSIONS)
def tests(session: Session) -> None:
    """Run the test suite with pytest."""
    args = session.posargs or []
    session.run("poetry", "install", "--no-dev", external=True)
    constrained_install(  # These are required for tests. Don't clutter w/ all dependencies!
        session,
        "coverage",
        "pytest",
        "pytest-clarity",
        "pytest-sugar",
        "pytest-mock",
        "pytest-cov",
        "typeguard",  # Though typing, run best in pytest
        "six",
    )
    session.run("pytest", *args)


@nox.session(python=VERSIONS)
def doc_tests(session: Session) -> None:
    """Test docstrings with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--no-dev", external=True)
    constrained_install(session, "xdoctest")
    session.run(
        "python",
        "-m",
        "xdoctest",
        "--verbose",
        "2",
        "--report",
        "cdiff",
        "--nocolor",
        PACKAGE,
        *args,
    )


@nox.session(python="3.9")
def doc_build(session: Session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    constrained_install(session, "sphinx", "sphinx-rtd-theme")
    session.run("sphinx-build", "docs", "docs/_build")
