# Dockerfile for FastAPI backend
FROM python:3.9-slim

# Set working directory
WORKDIR /back-end

# Install dependencies
COPY req_be.txt .
RUN pip install -r req_be.txt

# Copy the application
COPY . .

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
