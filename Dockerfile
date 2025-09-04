FROM astral/uv:python3.12-alpine
LABEL "org.opencontainers.image.source"="https://github.com/mrharishkumar/fastapi-cursor-boilerplate"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG DEV=false

COPY ./pyproject.toml /app/pyproject.toml
COPY ./uv.lock /app/uv.lock
COPY ./README.md /app/README.md

RUN apk add --update --no-cache unixodbc libstdc++ \
    && apk add --update --no-cache --virtual .tmp-build-deps build-base gcc musl-dev unixodbc-dev \
    && uv sync --locked --no-dev \
    && if [ "$DEV" = "true" ]; then uv pip install .[dev]; fi \
    && rm /app/pyproject.toml \
    && rm /app/uv.lock \
    && rm /app/README.md \
    && apk del .tmp-build-deps

COPY ./app /app/app
COPY ./tests /tmp/tests
COPY ./run.py /app/run.py

RUN adduser --disabled-password --gecos "" --home /app api-user && \
    chown -R api-user /app && \
    if [ "$DEV" = "true" ]; then \
        mv /tmp/tests /app/tests && \
        chown -R api-user:api-user /app/tests && \
        chmod -R 755 /app/tests; \
    else \
        rm -rf /tmp/tests; \
    fi

USER api-user

EXPOSE 8000

CMD ["uv", "run", "python", "run.py"]
