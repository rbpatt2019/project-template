# -*- coding: utf-8 -*-
"""Pytest configuration."""
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture


@pytest.fixture()
def mock_print(mocker: MockerFixture) -> Mock:
    """Mock the builtin print function."""
    return mocker.patch("builtins.print")
