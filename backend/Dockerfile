# Start with a Python 3.10 slim base image
FROM python:3.10.0-slim

# Update package list and install necessary Linux packages
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install psycopg2 (ensure you have requirements.txt if needed or install directly)
RUN pip install psycopg2==2.9.9

# Set the working directory in the Docker image
WORKDIR /app

# Copy your application's requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY . /app

#collect static files
RUN mkdir -p /app/staticfiles
#RUN python manage.py collectstatic --noinput

# Command to run your application
CMD ["gunicorn", "test_system.wsgi:application", "--bind", "0.0.0.0:8000"]

# Expose the port the app runs on
EXPOSE 8000
