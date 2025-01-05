# https://docs.astral.sh/uv/guides/integration/docker/
# https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile
# Above is a uv docker example

# base layer based on Linux Debian Bookworm
FROM python:3.12-slim-bookworm

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# install project dependencies
# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv venv .venv
RUN uv sync --frozen

# Presuming there is a `my_app` command provided by the project
CMD ["uv", "run", "run.py"]

