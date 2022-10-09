## Copier My controller

Copier template for scaffolding new my_controller upon [fastapi-mvc](https://github.com/fastapi-mvc/fastapi-mvc) project.

## Quickstart

To use this template outside `fastapi-mvc`:

Prerequisites:

* Python 3.8 or later [How to install python](https://docs.python-guide.org/starting/installation)
* Git 2.27 or newer
* copier 6.2.0 or later

```shell
copier copy "https://your.repo.url.here.git" /path/to/your/new/project
```

## Using Nix

```shell
nix-shell shell.nix
copier copy "https://your.repo.url.here.git" /path/to/your/new/project
```

## Updating

To update your generator with the changes from the [upstream](https://github.com/fastapi-mvc/copier-generator) run:

```shell
./update.sh
```

This action will not update/override your template and its configuration, but rather generators common files:

* Environment (`pyproject.toml` and `poetry.lock`)
* `README.md`
* Nix expression files
* dotfiles
* `LICENSE`

List of excluded files/paths:

* `template/**`
* `copier.yml`
* `*.py`
* `CHANGELOG.md`

Lastly, you can pass extra copier CLI options should you choose:

```shell
./update.sh -x README.md
```
