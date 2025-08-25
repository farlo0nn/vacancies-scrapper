FROM python:3.12-slim 


COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && curl -L https://github.com/jwilder/dockerize/releases/download/v0.7.0/dockerize-linux-amd64-v0.7.0.tar.gz \
    | tar -C /usr/local/bin -xz \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app 
COPY . .

RUN uv sync --locked

ENTRYPOINT ["dockerize"]
