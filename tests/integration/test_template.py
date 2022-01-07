import os


def test_cookiecutter_template(cookies):
    template_dir = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "../../fastapi_mvc/template",
        )
    )

    result = cookies.bake(
        template=template_dir,
        extra_context={
            "project_name": "myapp",
            "redis": "yes",
            "aiohttp": "yes",
            "github_actions": "yes",
            "vagrantfile": "yes",
            "helm": "yes",
            "author": "John Doe",
            "email": "jdoe@example.com",
            "repo_url": "https://test.repo",
            "year": "2022",
        }
    )

    assert result.exit_code == 0
