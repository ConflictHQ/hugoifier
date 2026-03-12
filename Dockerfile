# Use an official Python runtime as a parent image
FROM python:3.11.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose any necessary ports (if your application uses them)
# EXPOSE 8000

# Set environment variable for OpenAI API key (you may also pass this at runtime)
# ENV OPENAI_API_KEY=your_openai_api_key

# Define the command to run your application
CMD ["python3", "src/cli.py"]