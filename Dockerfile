# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p logs static

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000


# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "blog.wsgi:application"]
