import os

from fastapi_mvc.generators import ControllerGenerator


def test_controller_cookiecutter(cookies):
    result = cookies.bake(
        template=ControllerGenerator.template,
        extra_context={
            "package_name": "test_project",
            "folder_name": "test-project",
            "controller_name": "my_controller",
            "skip_routes": True,
            "controller_endpoints": {
                "index": "get",
                "create": "post"
            },
        },
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "test-project"
    assert result.project_path.is_dir()

    paths = [
        "test_project/app/controllers/my_controller.py",
        "tests/unit/app/controllers/test_my_controller.py",
    ]

    for path in paths:
        assert os.path.exists(
            os.path.join(result.project_path, path),
        )
