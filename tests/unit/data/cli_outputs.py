generate_root_help = """\
Usage: generate [OPTIONS] GENERATOR [ARGS]...

  Run chosen fastapi-mvc generator.

  The 'fastapi-mvc generate' commands runs a generator of your choice for a
  fastapi-mvc project at the current working directory.

Options:
  --help  Show this message and exit.

Please choose a generator below.

Builtins:
  controller
  generator

UnitTests:
  foobar
  my_controller
"""


generate_generator_help = """\
Usage: generate generator [OPTIONS] NAME

Options:
  -S, --skip  Skip files that already exist.
  --help      Show this message and exit.

{usage}
"""


generate_controller_help = """\
Usage: generate controller [OPTIONS] NAME [ENDPOINTS]...

Options:
  -S, --skip         Skip files that already exist.
  -R, --skip-routes  Weather to skip routes entry
  --help             Show this message and exit.

{usage}
"""
