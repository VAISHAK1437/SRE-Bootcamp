# Stage 1: Build the application
FROM python:3.11-alpine AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies
RUN apk add --no-cache build-base libffi-dev

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Copy application code
COPY . .

# Stage 2: Production image
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/usr/local/bin:$PATH"

# Install runtime dependencies
RUN apk add --no-cache libffi

# Set the working directory
WORKDIR /app

# Copy installed dependencies and application code from the builder stage
COPY --from=builder /install /usr/local
COPY --from=builder /app /app

# Expose the Flask port
EXPOSE 5000

# Command to run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
