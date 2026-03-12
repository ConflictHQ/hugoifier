# Use an official Python runtime as a parent image
FROM python:3.11.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install package and dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy the rest of the application code into the container
COPY . .

CMD ["hugoifier"]