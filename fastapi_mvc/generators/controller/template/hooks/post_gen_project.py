"""Fastapi-mvc cookiecutter controller template post_gen_project hook."""
import os


def edit_router():
    """Add import and router entry to config/router.rb if not skipped."""
    if not {{cookiecutter.skip_routes}}:
        router = os.path.join(
            os.getcwd(), "{{cookiecutter.package_name}}/app/router.py"
        )
        import_str = "from {0:s}.app.controllers import {1:s}\n".format(
            "{{cookiecutter.package_name}}",
            "{{cookiecutter.controller_name}}",
        )

        with open(router, "r") as f:
            lines = f.readlines()

        if import_str in lines:
            return

        for i in range(len(lines)):
            if lines[i].strip() == "from fastapi import APIRouter":
                index = i + 1
                break
        else:
            index = 0

        lines.insert(index, import_str)
        lines.append(
            "root_api_router.include_router({{cookiecutter.controller_name}}.router)\n"
        )

        with open(router, "w") as f:
            f.writelines(lines)


if __name__ == "__main__":
    edit_router()
