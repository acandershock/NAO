# Dockerfile for LLM

# Chose the base image (slim buster is more lightweight)
FROM python:3.9.14-slim-buster

# Set working directory (like cd) inside the container
WORKDIR /app

# Upgrade pip to download requirements.txt
RUN pip install --upgrade pip

# Copy requirements.txt into app and install dependencies
# --no-cache-dir keeps from downloading
COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files to /app working dir
COPY . .

# Add SDK to path in python
ENV PYTHONPATH='/app/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327:$PYTHONPATH'

# Run executable on first startup
CMD ["python", "send_requestLLM.py"]