# Use the official Python image with version 3.9
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libpq-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable for Django settings
ENV DJANGO_SETTINGS_MODULE="povertymappingapp.settings"

# Run the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "povertymappingapp.wsgi:application"]
