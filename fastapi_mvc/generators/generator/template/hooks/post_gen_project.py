"""Fastapi-mvc cookiecutter generator template post_gen_project hook."""
import os


def add_root_dirs():
    """Add template root directories."""
    template_dir = "lib/generators/{{cookiecutter.generator_name}}/template"

    root_dir = os.path.join(
        template_dir, "{% raw %}{{cookiecutter.folder_name}}{% endraw %}"
    )
    package_dir = os.path.join(
        root_dir, "{% raw %}{{cookiecutter.package_name}}{% endraw %}"
    )
    hooks_dir = os.path.join(template_dir, "hooks")

    try:
        os.mkdir(root_dir)
    except OSError:
        pass

    try:
        os.mkdir(package_dir)
    except OSError:
        pass

    try:
        os.mkdir(hooks_dir)
    except OSError:
        pass


if __name__ == "__main__":
    add_root_dirs()
