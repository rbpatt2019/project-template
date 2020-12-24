# -*- coding: utf-8 -*-
import pytest

from project_template import __version__, console


def test_main_called(mock_print):
    """It calls the function"""
    console.main()
    assert mock_print.called


def test_main_args(mock_print):
    """It is called with the current version"""
    console.main()
    args, _ = mock_print.call_args
    assert f"Project is version {__version__}" in args[0]


def test_main_exception(mock_print):
    """It fails as expected"""
    mock_print.side_effect = Exception("This is forced!")
    with pytest.raises(Exception):
        console.main()
