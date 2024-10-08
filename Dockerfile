# Stage 1: Builder
FROM python:3.11 AS builder

# Improve performance and prevent generation of .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Create and activate a virtual environment, then install the dependencies
RUN pip install virtualenv && \
    virtualenv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Deployer
FROM python:3.11-slim AS deployer

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the rest of the application code
COPY . .

EXPOSE 8001
