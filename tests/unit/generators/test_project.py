import os

import pytest
import mock
from fastapi_mvc.generators import ProjectGenerator
from cookiecutter.exceptions import OutputDirExistsException


template_dir = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../../../fastapi_mvc/template",
    )
)


@pytest.fixture
def pg():
    yield ProjectGenerator()


@pytest.mark.parametrize(
    "context, output_dir",
    [
        (
            {
                "project_name": "testapp",
                "redis": "yes",
                "aiohttp": "yes",
                "github_actions": "yes",
                "vagrantfile": "yes",
                "helm": "yes",
                "codecov": "yes",
                "author": "John Doe",
                "email": "example@email.com",
                "repo_url": "https://your.repo.url.here",
                "year": "2022",
                "fastapi_mvc_version": "x.y.z",
            },
            "/test/path",
        ),
        (
            {
                "project_name": "testapp",
                "redis": "no",
                "aiohttp": "no",
                "github_actions": "no",
                "vagrantfile": "no",
                "helm": "no",
                "codecov": "no",
                "author": "Joe",
                "email": "email@test.com",
                "repo_url": "https://your.repo.url.here",
                "year": "2022",
                "fastapi_mvc_version": "x.y.z",
            },
            "/my/awesome/projects",
        ),
    ],
)
@mock.patch("fastapi_mvc.generators.project.cookiecutter")
def test_new(cookie_mock, pg, context, output_dir):
    pg.new(context, output_dir)
    cookie_mock.assert_called_once_with(
        template_dir,
        extra_context=context,
        no_input=True,
        output_dir=output_dir,
    )


@mock.patch(
    "fastapi_mvc.generators.project.cookiecutter",
    side_effect=OutputDirExistsException(),
)
def test_new_dir_exists(cookie_mock, pg):
    with pytest.raises(OutputDirExistsException):
        pg.new({}, "/test/path")

    cookie_mock.assert_called_once_with(
        template_dir,
        extra_context={},
        no_input=True,
        output_dir="/test/path",
    )
