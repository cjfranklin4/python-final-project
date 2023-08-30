# Use an official Python runtime as the base image
FROM python:3.8-slim-buster

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the everything that is in this repo and put it into the directory
COPY . .

# Install Flask library
RUN pip install flask

# Make the /data directory inside the container to store the SQLite3 database
RUN mkdir /data
COPY inventory.db /data/inventory.db
# Run app.py when the container launches
CMD ["python", "main.py"]
