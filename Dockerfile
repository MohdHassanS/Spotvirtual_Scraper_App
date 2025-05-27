# Use official Python base image
FROM python:3.11-slim

# Install dependencies for Chromium + ChromeDriver + Selenium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    unzip \
    xvfb \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    fonts-liberation \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome and headless
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_PATH=/usr/lib/chromium/

# Set working directory inside container
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire app code to the container
COPY . .

# Expose the port Streamlit uses
EXPOSE 8000

# Run Streamlit app on container startup
CMD ["streamlit", "run", "spot.py", "--server.port=8000", "--server.address=0.0.0.0", "--server.headless=true"]
