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

# Command to run the Flask app
CMD ["gunicorn", "-w", "3", "app:app", "-b", "0.0.0.0:8080"]
