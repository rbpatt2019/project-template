import nox
import tempfile

LOCATIONS = ["src", "tests", "noxfile.py"]
VERSIONS = ["3.9", "3.8", "3.7"]


def constrained_install(session, *args, **kwargs):
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
def format(session):
    args = session.posargs or LOCATIONS
    constrained_install(session, "black")
    session.run("black", *args)


@nox.session(python=VERSIONS)
def lint(session):
    # As pylint requires installed packages and nox spins off isolated venvs,
    # Import error is silenced. This is checked by pyright, and helps
    # prevent lengthy installs
    args = session.posargs or LOCATIONS
    constrained_install(session, "pylint")
    session.run("pylint", "--disable=import-error", *args)


@nox.session(python=VERSIONS)
def tests(session):
    args = session.posargs or []

    # Install app requirements generally
    session.run("poetry", "install", "--no-dev", external=True)
    # Install testing requirements explicitly
    constrained_install(
        session,
        "coverage",
        "pytest",
        "pytest-clarity",
        "pytest-sugar",
        "pytest-mock",
        "pytest-cov",
        "six",
    )

    session.run("pytest", *args)
