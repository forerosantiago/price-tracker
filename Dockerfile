# Use the official Python image as a base
FROM python:3.9-slim

# Install Firefox, Geckodriver and Sqlite3
RUN apt-get update && apt-get install -y \
    firefox-esr sqlite3

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Command to run the application
CMD ["python", "db_setup.py"]
CMD ["python", "main.py"]
