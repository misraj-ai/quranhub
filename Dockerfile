FROM python:alpine

# Install system dependencies (including PostgreSQL development libraries)
RUN apk update && \
    apk add --no-cache \
    build-base \
    libsndfile-dev \
    postgresql-dev

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the entire application directory into the working directory
COPY . /app/

# Expose the specified port
EXPOSE 8080

# Run the Python script
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
