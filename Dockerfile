FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system deps for building (minimal) and cleanup
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000
ENV PORT=8000

# Use shell form so environment variables expand at runtime
CMD sh -c "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"
