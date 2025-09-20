# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose port
EXPOSE 8000

# Run app with reload in dev
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
