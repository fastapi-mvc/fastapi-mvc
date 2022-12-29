#! /usr/bin/env nix-shell
#! nix-shell shell.nix -i bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

copier -x template/** -x copier.yml.keep -x *.py -x CHANGELOG.md \
  "${@}" \
  -d generator=foobar \
  -d nix=True \
  -d license=MIT \
  -d repo_url=https://your.repo.url.here \
  -d copyright_date=2022 \
  -a .generator.yml \
  update ./.
