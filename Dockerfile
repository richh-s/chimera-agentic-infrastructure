FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Clean any existing pip cache
RUN pip cache purge

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install uv if not already installed
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv

RUN uv pip install --system --group dev --no-cache

COPY . .

ENTRYPOINT ["sh", "-c"]
CMD ["pytest"]