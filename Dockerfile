# syntax=docker/dockerfile:1.3
FROM seculayer/python:3.7 AS builder
LABEL maintainer="jinkim jinkim@seculayer.com"

ARG APP_DIR="/opt/app"
ARG POETRY_VERSION=1.1.13

ENV POETRY_VIRTUALENVS_IN_PROJECT=1 \
    PATH="/root/.local/bin:$PATH"

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install install pipx
RUN pipx ensurepath
RUN pipx install "poetry==$POETRY_VERSION"

WORKDIR ${APP_DIR}

COPY pyproject.toml poetry.lock ${APP_DIR}

RUN --mount=type=secret,id=gitconfig,target=/root/.gitconfig,required=true \
    --mount=type=secret,id=cert,required=true \
    # --mount=type=cache,target=/root/.cache/pypoetry/cache \
    # --mount=type=cache,target=/root/.cache/pypoetry/artifacts \
    poetry install --no-dev --no-root --no-interaction --no-ansi


FROM seculayer/python:3.7 AS app
ARG APP_DIR="/opt/app"
ARG CLOUD_AI_DIR="/eyeCloudAI/app/ape/eda/"
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8

RUN mkdir -p ${CLOUD_AI_DIR}
WORKDIR ${CLOUD_AI_DIR}

RUN groupadd -g 1000 aiuser
RUN useradd -r -u 1000 -g aiuser aiuser
RUN chown -R aiuser:aiuser /eyeCloudAI
USER aiuser

COPY --chown=aiuser:aiuser --from=builder ${APP_DIR}/.venv ${CLOUD_AI_DIR}/.venv
COPY --chown=aiuser:aiuser eda ${CLOUD_AI_DIR}/eda
COPY --chown=aiuser:aiuser eda.sh ${CLOUD_AI_DIR}
RUN chmod +x ${CLOUD_AI_DIR}/eda.sh

ENV PATH="${CLOUD_AI_DIR}/.venv/bin:$PATH"

CMD ["${CLOUD_AI_DIR}/eda.sh"]
