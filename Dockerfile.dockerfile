# Use the official Python image as a base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for the Flask app
EXPOSE 8080

# Set the environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

FROM debian:latest

# Install 'dash' and link it to /bin/sh
RUN apt-get update && apt-get install -y dash \
    && ln -sf /bin/dash /bin/sh

# Verify 'sh' availability
RUN sh -c "echo 'sh is available in this Docker image'"

# Command to run the Flask app
CMD ["gunicorn", "-w", "3", "app:app", "-b", "0.0.0.0:8080"]
