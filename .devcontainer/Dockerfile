FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
curl \
git \
git-lfs \
&& rm -rf /var/lib/apt/list/*

RUN git lfs install --system

Run curl -LsSf https:// astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

RUN uv venv .venv

COPY requirements.txt.

RUN uv pip install --python .venv/bin/python -r requirements.txt

ENV VIRTUAL:ENV=/app/.venv

ENV PATH="/app/.venv/bin:$PATH"

