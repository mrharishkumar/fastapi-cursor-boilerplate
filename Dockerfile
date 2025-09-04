FROM astral/uv:python3.12-alpine
LABEL "org.opencontainers.image.source"="https://github.com/mrharishkumar/fastapi-cursor-boilerplate"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG DEV=false

COPY ./pyproject.toml /app/pyproject.toml
COPY ./uv.lock /app/uv.lock
COPY ./README.md /app/README.md

RUN arch="$(uname -m)" && \
    case "$arch" in \
    x86_64) architecture="amd64" ;; \
    aarch64|arm64) architecture="arm64" ;; \
    *) echo "Unsupported Alpine architecture: $arch" >&2; exit 1;; \
    esac && \
    apk add --update --no-cache curl unixodbc libstdc++ \
    && curl -O https://download.microsoft.com/download/fae28b9a-d880-42fd-9b98-d779f0fdd77f/msodbcsql18_18.5.1.1-1_$architecture.apk \
    && apk add --allow-untrusted msodbcsql18_18.5.1.1-1_${architecture}.apk \
    && apk add --update --no-cache --virtual .tmp-build-deps build-base gcc musl-dev unixodbc-dev \
    && uv sync --locked --no-dev \
    && if [ "$DEV" = "true" ]; then uv pip install .[dev]; fi \
    && rm msodbcsql18_18.5.1.1-1_$architecture.apk \
    && rm /app/pyproject.toml \
    && rm /app/uv.lock \
    && rm /app/README.md \
    && apk del curl \
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
