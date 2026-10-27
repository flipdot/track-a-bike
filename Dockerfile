FROM python:3.12-slim

# graphviz for the dot visualizations
RUN apt-get update \
    && apt-get install -y --no-install-recommends graphviz \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv venv .venv && uv sync --frozen --no-dev

COPY src ./

# The pipeline expects a Neo4j server at bolt://localhost:7687.
# Run one as a sidecar, e.g.: docker run -p 7687:7687 neo4j:5
ENTRYPOINT [".venv/bin/python", "app.py"]
