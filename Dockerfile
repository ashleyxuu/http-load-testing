# Use the official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages
RUN pip install --no-cache-dir aiohttp pytest pytest-aiohttp

# Set the default command to run when the container starts
ENTRYPOINT ["python", "load_tester.py"]
