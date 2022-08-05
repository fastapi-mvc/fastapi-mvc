import pytest
from unittest import mock

from fastapi_mvc.commands import RunGenerator


@pytest.mark.parametrize(
    "options",
    [
        {
            "foo": "bar",
            "val": 123,
        },
        {
            "skip_redis": True,
            "skip_aiohttp": True,
            "skip_vagrantfile": True,
            "skip_helm": True,
            "skip_actions": True,
            "skip_codecov": True,
            "skip_install": False,
            "license": "ISC",
            "repo_url": "https://scm.test/repo",
        },
    ],
)
def test_execute(options):
    generator = mock.Mock()
    generator.name = "test-gen"

    command = RunGenerator(
        generator=generator,
        options=options,
    )
    command.execute()

    generator.new.assert_called_once_with(**options)
