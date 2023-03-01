import pytest
from fastapi_mvc.utils import run_shell


def dirhash(path):
    """Calculate directory sha256sum using bash magic.

    The bellow code will execute the following shell command:
    ``find . -type f ! -path "./.git/*" -print0 | xargs -0 sha256sum | sort | sha256sum``

    """
    # First, find all the files inside the current working directory,
    # excluding .git/* path.
    find_ps = run_shell(
        cmd=["find", ".", "-type", "f", "!", "-path", "./.git/*", "-print0"],
        cwd=path,
        check=True,
        capture_output=True
    )
    # Calculate sha256sum for each file found.
    xargs_ps = run_shell(
        cmd=["xargs", "-0", "sha256sum"],
        cwd=path,
        input=find_ps.stdout,
        check=True,
        capture_output=True
    )
    # Sort results.
    sort_ps = run_shell(
        cmd=["sort"],
        cwd=path,
        input=xargs_ps.stdout,
        check=True,
        capture_output=True
    )
    # Calculate sha256sum for sorted results to get "reduced" checksum.
    checksum_ps = run_shell(
        cmd=["sha256sum"],
        cwd=path,
        input=sort_ps.stdout,
        check=True,
        capture_output=True
    )
    return checksum_ps.stdout


class TestCliUpdateCommand:

    @pytest.mark.parametrize("old, target", [
        ("0.1.0", "0.5.0"),
        ("0.1.1", "0.5.0"),
        ("0.2.0", "0.5.0"),
        ("0.3.0", "0.5.0"),
        ("0.4.0", "0.5.0"),
    ])
    def test_should_update_outdated_project_to_given_version(self, tmp_path, monkeypatch, new_copy, update_copy, cli_runner, reference_projects, old, target):
        # given
        old_project = tmp_path / "update-test"
        old_project.mkdir(parents=True)
        create_result = cli_runner.invoke(
            new_copy,
            [
                "--skip-install",
                "--no-interaction",
                "--use-version",
                old,
                str(old_project),
            ],
        )
        # make sure project was generated successfully
        assert create_result.exit_code == 0
        monkeypatch.chdir(str(old_project))
        run_shell(["git", "config", "user.email", "git@jdoe.com"], check=True)
        run_shell(["git", "config", "user.name", "John Doe"], check=True)
        run_shell(["git", "add", "."], check=True)
        run_shell(["git", "commit", "-m", "Initial commit"], check=True)

        # when
        update_result = cli_runner.invoke(
            update_copy,
            [
                "--no-interaction",
                "--use-version",
                target,
            ],
        )

        # then
        assert update_result.exit_code == 0
        assert dirhash(str(old_project)) == dirhash(str(reference_projects[target]))

    def test_should_not_update_when_git_dirty(self, update_copy, default_project, cli_runner, monkeypatch):
        # given
        monkeypatch.chdir(default_project)

        # when
        result = cli_runner.invoke(
            update_copy,
            [
                "--no-interaction",
                "--use-version",
                "master",
            ],
        )

        # then
        assert result.exit_code == 2
        assert result.output.startswith("Destination repository is dirty")
