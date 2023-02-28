from unittest import mock

from fastapi_mvc import Generator, Command
from fastapi_mvc.constants import ANSWERS_FILE


class TestCommand:

    def test_should_create_command_and_populate_defaults(self):
        # given / when
        command = Command(name="fake-command")

        # then
        assert command.name == "fake-command"
        assert not command.alias
        assert not command.project_data


class TestGenerator:

    def test_should_create_generator_and_populate_defaults(self):
        # given / when
        generator = Generator(name="fake-generator", template="https://fake.repo.git")

        # then
        assert generator.template == "https://fake.repo.git"
        assert not generator.vcs_ref
        assert generator.category == "Other"


class TestGeneratorRunCopy:

    @mock.patch("fastapi_mvc.core.copier")
    def test_should_call_copier_run_copy_with_defaults(self, copier_mock):
        # given
        generator = Generator(
            name="fake-generator",
            template="https://fake.repo.git",
            vcs_ref="master",
            category="Fake",
        )

        # when
        generator.run_copy(dst_path="/tmp/test", data={"foo": "bar"})

        # then
        copier_mock.run_copy.assert_called_once_with(
            src_path=generator.template,
            dst_path="/tmp/test",
            vcs_ref=generator.vcs_ref,
            answers_file=ANSWERS_FILE,
            data={"foo": "bar"},
        )


class TestGeneratorRunUpdate:

    @mock.patch("fastapi_mvc.core.copier")
    def test_should_call_copier_run_update_with_defaults(self, copier_mock):
        # given
        generator = Generator(
            name="fake-generator",
            template="https://fake.repo.git",
            vcs_ref="master",
            category="Fake",
        )

        # when
        generator.run_update(dst_path="/tmp/test", data={"foo": "bar"})

        # then
        copier_mock.run_update.assert_called_once_with(
            dst_path="/tmp/test",
            vcs_ref=generator.vcs_ref,
            answers_file=ANSWERS_FILE,
            data={"foo": "bar"},
        )
