import os


template_dir = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../../fastapi_mvc/template",
    )
)


def test_cookiecutter_template(cookies):
    result = cookies.bake(
        template=template_dir,
        extra_context={
            "project_name": "test-project",
            "redis": "yes",
            "aiohttp": "yes",
            "github_actions": "yes",
            "vagrantfile": "yes",
            "helm": "yes",
            "codecov": "yes",
            "author": "John Doe",
            "email": "jdoe@example.com",
            "repo_url": "https://test.repo",
            "year": "2022",
        },
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "test-project"
    assert result.project_path.is_dir()


def test_cookiecutter_template_minimal(cookies):
    result = cookies.bake(
        template=template_dir,
        extra_context={
            "project_name": "test-project",
            "redis": "no",
            "aiohttp": "no",
            "github_actions": "no",
            "vagrantfile": "no",
            "helm": "no",
            "codecov": "no",
            "author": "John Doe",
            "email": "jdoe@example.com",
            "repo_url": "https://test.repo",
            "year": "2022",
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
        "Vagrantfile",
    ]

    for path in paths:
        assert not os.path.exists(
            os.path.join(result.project_path, path),
        )
