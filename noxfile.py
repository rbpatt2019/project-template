import multiprocessing
import tempfile

import nox

LOCATIONS = ["src", "tests", "noxfile.py"]
VERSIONS = ["3.9", "3.8", "3.7"]
CORES = int(multiprocessing.cpu_count() / 2)

# There's a good chance that this will get refactored out if I move to pyup
# which requires a requirements.txt file
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
def form(session):
    args = session.posargs or LOCATIONS
    constrained_install(session, "isort", "black")
    session.run("isort", *args)
    session.run("black", *args)


@nox.session(python=VERSIONS)
def security(session):
    # I'd like to move skip to config file, but bandit doesn't yet support pyproject
    args = session.posargs or LOCATIONS
    constrained_install(session, 'safety', 'bandit')
    session.run('bandit', '--skip=B101', '-r', *args) 
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
        session.run("safety", "check", f'--file={reqs.name}', '--full-report')

@nox.session(python=VERSIONS)
def lint(session):
    # As pylint requires installed packages and nox spins off isolated venvs,
    # Import error is silenced. This is checked by pyright, and helps
    # prevent lengthy installs
    args = session.posargs or LOCATIONS
    constrained_install(session, "pylint")
    session.run("pylint", "--disable=import-error", f'-j {CORES}', *args)


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
