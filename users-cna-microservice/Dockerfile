FROM python:3.10-slim-bullseye

# Optional build deps (only needed if your packages compile native code)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser
USER appuser

WORKDIR /app

# Copy requirements first for better caching and install
COPY --chown=appuser:appuser requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source
COPY --chown=appuser:appuser . .

# Ensure logs flush immediately
ENV PYTHONUNBUFFERED=1

# Make sure your app listens on 0.0.0.0:9090
EXPOSE 9090

# Start the app (adjust if you use uvicorn directly)
CMD ["python", "app.py"]
