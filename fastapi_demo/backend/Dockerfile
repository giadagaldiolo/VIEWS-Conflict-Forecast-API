# Use official Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory inside the container to /app
WORKDIR /app

# Copy only requirements.txt first to leverage Docker layer caching
COPY backend/requirements.txt .

# Install Python dependencies without pip cache to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend source code into the container
COPY backend/ .

# Expose port 8000 (FastAPI default port) for external access and documentation
EXPOSE 8000

# Run the FastAPI app using uvicorn with host 0.0.0.0 to allow outside connections
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
