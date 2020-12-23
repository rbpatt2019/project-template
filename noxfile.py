import nox
import tempfile

def constrained_install(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as reqs:
        session.run('poetry', 'export', '--dev', '--format=requirements.txt', f'--output={regs.name}', external=True)
        session.install(f'--constraint={regs.name}', *args, **kwargs)

@nox.session(python=["3.9", "3.8", "3.7"])
def tests(session):
    args = session.posargs or []

    # Install app requirements generally
    session.run("poetry", "install", '--no-dev', external=True)
    # Install testing requirements explicitly
    constrained_install(session, 'coverage', 'pytest', 'pytest-clarity', 'pytest-sugar', 'pytest-mock', 'pytest-cov', 'six')

    session.run("pytest")
