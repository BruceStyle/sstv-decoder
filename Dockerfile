FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.11.2 /uv /usr/local/bin/uv

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --no-create-home decoder

WORKDIR /app
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    OPENBLAS_NUM_THREADS=1

COPY pyproject.toml LICENSE README.md ./
COPY src ./src
RUN uv pip install --system --no-cache .

USER decoder
EXPOSE 8000
CMD ["uvicorn", "sstv_decoder.mcp_http:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
