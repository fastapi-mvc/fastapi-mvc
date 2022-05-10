import os

from fastapi_mvc.generators import ProjectGenerator


def test_cookiecutter_template(cookies):
    result = cookies.bake(
        template=ProjectGenerator.template,
        extra_context={
            "project_name": "test-project",
            "redis": "yes",
            "aiohttp": "yes",
            "github_actions": "yes",
            "helm": "yes",
            "author": "John Doe",
            "email": "jdoe@example.com",
            "license": "MIT",
            "repo_url": "https://test.repo",
            "year": "2022",
            "fastapi_mvc_version": "x.y,z",
        },
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "test-project"
    assert result.project_path.is_dir()


def test_cookiecutter_template_minimal(cookies):
    result = cookies.bake(
        template=ProjectGenerator.template,
        extra_context={
            "project_name": "test-project",
            "redis": "no",
            "aiohttp": "no",
            "github_actions": "no",
            "helm": "no",
            "author": "John Doe",
            "email": "jdoe@example.com",
            "license": "ISC",
            "repo_url": "https://test.repo",
            "year": "2022",
            "fastapi_mvc_version": "x.y,z",
        },
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "test-project"
    assert result.project_path.is_dir()

    paths = [
        "charts",
        ".github",
        "build/dev-env.sh",
        "manifests",
        "tests/unit/app/utils/test_aiohttp_client.py",
        "test_project/app/utils/aiohttp_client.py",
    ]

    for path in paths:
        assert not os.path.exists(
            os.path.join(result.project_path, path),
        )
