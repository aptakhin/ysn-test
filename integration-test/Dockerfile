FROM python:3.10.0-buster

ARG PIP_VERSION
ARG POETRY_VERSION

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/ysn

RUN pip install --upgrade pip==${PIP_VERSION} poetry==${POETRY_VERSION}

COPY poetry.lock pyproject.toml /app/
WORKDIR /app/

RUN  poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /app
