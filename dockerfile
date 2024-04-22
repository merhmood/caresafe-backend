# Use the official Python base image
FROM python:3.9-slim as dev

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

ENV JWT_SECRET_KEY dev
ENV SECRET_KEY dev

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 8000

# Set the entrypoint command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]





# Use the official Python base image
FROM python:3.9-slim as prod

ENV JWT_SECRET_KEY production
ENV SECRET_KEY production

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 8000

# Set the entrypoint command to run the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "service:app"]