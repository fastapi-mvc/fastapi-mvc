FROM alpine@sha256:e7d88de73db3d3fd9b2d63aa7f447a10fd0220b7cbf39803c803f2af9ba256b3 as builder
LABEL maintainer="{{cookiecutter.author}}, {{cookiecutter.email}}"

COPY . /{{cookiecutter.folder_name}}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_HOME=/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apk --no-cache add gcc clang build-base libffi-dev python3 python3-dev curl && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 - && \
    cd /{{ cookiecutter.folder_name }} && \
    poetry install --no-dev --no-interaction

FROM alpine@sha256:e7d88de73db3d3fd9b2d63aa7f447a10fd0220b7cbf39803c803f2af9ba256b3
LABEL maintainer="{{cookiecutter.author}}, {{cookiecutter.email}}"

RUN apk --no-cache add python3

COPY --from=builder /{{cookiecutter.folder_name}} /{{cookiecutter.folder_name}}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/{{cookiecutter.folder_name}}/.venv/bin:$PATH"

EXPOSE 8000/tcp

STOPSIGNAL SIGINT

CMD ["/{{cookiecutter.folder_name}}/.venv/bin/{{cookiecutter.script_name}}", "serve", "--host", "0.0.0.0"]
