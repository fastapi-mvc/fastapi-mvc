# This digest SHA points to python:3.13-slim-trixie tag
FROM python@sha256:3de9a8d7aedbb7984dc18f2dff178a7850f16c1ae7c34ba9d7ecc23d0755e35f AS builder
LABEL maintainer="Radosław Szamszur, radoslawszamszur@gmail.com"

# Configure environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=0 \
    SOURCE_DATE_EPOCH=0 \
    CFLAGS=-g0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    UV_INSTALL_DIR=/opt/uv \
    UV_PROJECT_ENVIRONMENT="/venv" \
    UV_VERSION=0.10.0 \
    UV_INSTALL_OPTS="--no-editable --no-extra test --no-extra docs" \
    WORKDIR="/pysetup"

ENV PATH="${UV_INSTALL_DIR}:${UV_PROJECT_ENVIRONMENT}/bin:${PATH}"

# Configure Debian snapshot archive
RUN echo "deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/20260206 trixie main" > /etc/apt/sources.list && \
    echo "deb [check-valid-until=no] http://snapshot.debian.org/archive/debian-security/20260206 trixie-security main" >> /etc/apt/sources.list && \
    echo "deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/20260206 trixie-updates main" >> /etc/apt/sources.list

# Install build tools and dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y curl build-essential git

COPY . $WORKDIR
WORKDIR $WORKDIR
RUN make install

# Override virtualenv Python symlink to Python path in gcr.io/distroless/python3 image
RUN ln -fns /usr/bin/python $UV_PROJECT_ENVIRONMENT/bin/python

# Use distroless Python3 image, locked to digest SHA in order to have deterministic Python version - 3.13.5.
# For the time being, gcr.io/distroless/python3 doesn't have any tags to particular minor version.
# This digest SHA points to python3:nonroot
FROM gcr.io/distroless/python3@sha256:e8c7ab4451b52873053d716496be1b88db8cc82370600fbaf1ddafd7c67da6da
LABEL maintainer="Radosław Szamszur, radoslawszamszur@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT="/venv"

COPY --from=builder $UV_PROJECT_ENVIRONMENT $UV_PROJECT_ENVIRONMENT

ENV PATH="${UV_PROJECT_ENVIRONMENT}/bin:${PATH}"

USER nonroot

STOPSIGNAL SIGINT

ENTRYPOINT ["fastapi-mvc"]
