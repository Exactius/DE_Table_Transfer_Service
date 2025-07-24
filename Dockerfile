FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Cloud Run provides PORT environment variable
EXPOSE 8080

# Start the application
CMD ["python", "main.py"]