import os

import mock
import pytest
from click import BadParameter
from {{cookiecutter.package_name}}.cli.utils import validate_directory


current_dir = os.path.dirname(__file__)


def test_validate_directory():
    result = validate_directory(mock.MagicMock(), mock.MagicMock(), current_dir)
    assert result == current_dir

    with pytest.raises(BadParameter):
        validate_directory(
            mock.MagicMock(), mock.MagicMock(), "/path/does/not/exist"
        )

    with mock.patch("{{cookiecutter.package_name}}.cli.utils.os.access") as mck:
        mck.return_value = False

        with pytest.raises(BadParameter):
            validate_directory(
                mock.MagicMock(), mock.MagicMock(), os.path.abspath(__file__)
            )

        mck.assert_called_once_with(current_dir, os.W_OK)