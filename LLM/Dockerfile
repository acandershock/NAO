# Dockerfile for LLM

# Chose the base image (slim buster is more lightweight)
FROM python:2.7-slim-buster

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

# Copy the SDK tarball into the container
COPY pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327.tar.gz /app/

# Extract the SDK inside the container
RUN tar -xvzf pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327.tar.gz

# Add SDK to path in python
ENV PYTHONPATH='/app/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327/lib/python2.7/site-packages:$PYTHONPATH'
ENV LD_LIBRARY_PATH='/app/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327/lib/python2.7/site-packages:$LD_LIBRARY_PATH'

# Run executable on first startup
CMD ["python", "send_requestLLM.py"]