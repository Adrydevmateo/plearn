# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for WeasyPrint (rendering PDFs)
RUN apt-get update \
    && apt-get install -y \
    libpango1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libjpeg62-turbo \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application into the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
