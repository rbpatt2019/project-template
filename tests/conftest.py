# -*- coding: utf-8 -*-
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def mock_print(mocker: MockerFixture) -> Mock:
    return mocker.patch("builtins.print")
