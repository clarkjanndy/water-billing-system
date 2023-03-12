# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /water-billing-system

# Copy the requirements file into the container
COPY requirements.txt .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 8000 for the application to run on
EXPOSE 8000

# Set the command to run the application when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]