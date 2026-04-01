# Dockerfile

# 1 Use official Python slim image
FROM python:3.12-slim

# 2 Set working directory inside the container
WORKDIR /app

# Install netcat
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# 3 Copy requirements first for caching
COPY requirements.txt .

# 4 Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5 Copy the rest of the app
COPY . .

# 6 Expose FastAPI port
EXPOSE 8000

# 7 Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]