import pytest


@pytest.fixture
def mock_print(mocker):
    return mocker.patch("builtins.print")
