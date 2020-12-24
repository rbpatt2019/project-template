# -*- coding: utf-8 -*-
import multiprocessing
import tempfile
from typing import Any, List

# pylint: disable=import-error
import nox  # type: ignore
from nox.sessions import Session  # type: ignore

LOCATIONS: List[str] = ["src", "tests", "noxfile.py"]
PACKAGE: str = "project_template"
VERSIONS: List[str] = ["3.9", "3.8", "3.7"]
CORES: int = int(multiprocessing.cpu_count() / 2)

nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = True

# There's a good chance that this will get refactored out if I move to pyup
# which requires a requirements.txt file
def constrained_install(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages with poetry version constraint"""
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
    """Format code with isort and black"""
    args = session.posargs or LOCATIONS
    constrained_install(session, "isort", "black")
    session.run("isort", *args)
    session.run("black", *args)


@nox.session(python=VERSIONS)
def security(session: Session) -> None:
    """Check security with bandit and safety"""
    # I'd like to move skip to config file, but bandit doesn't yet support pyproject
    args = session.posargs or LOCATIONS
    constrained_install(session, "safety", "bandit")
    session.run("bandit", "--skip=B101", "-r", *args)
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
def lint(session: Session) -> None:
    """Lint files with pylint and pyright"""
    args = session.posargs or LOCATIONS
    session.run("poetry", "install", "--no-dev", external=True)  # To check imports
    # Pytest required to prevent error
    constrained_install(session, "pylint", "darglint", "pytest", "pytest-mock")
    session.run("pylint", f"-j {CORES}", *args)
    session.run("pyright", *args, external=True)  # I'd prefer a local install...
    session.run(
        "darglint", "-s", "numpy", "-z", "short", "-v", "2", "-l", "DEBUG", *args
    )


@nox.session(python=VERSIONS)
def tests(session: Session) -> None:
    """Run the test suite with pytest"""
    args = session.posargs or []
    session.run("poetry", "install", "--no-dev", external=True)
    constrained_install(  # These are required for tests. Don't clutter w/ all dev deps!
        session,
        "coverage",
        "pytest",
        "pytest-clarity",
        "pytest-sugar",
        "pytest-mock",
        "pytest-cov",
        "typeguard",
        "six",
    )
    session.run("pytest", *args)


@nox.session(python=VERSIONS)
def doc_tests(session: Session) -> None:
    """Test docstrings with xdoctest"""
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
        PACKAGE,
        *args,
    )


@nox.session(python="3.9")
def doc_build(session: Session) -> None:
    """Build the documentation"""
    session.run("poetry", "install", "--no-dev", external=True)
    constrained_install(session, "sphinx", "sphinx-rtd-theme")
    session.run("sphinx-build", "docs", "docs/_build")
