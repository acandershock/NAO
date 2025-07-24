# Dockerfile for LLM

# Chose the base image (slim buster is more lightweight)
FROM python3.9

# Set working directory (like cd) inside the container
WORKDIR /app

# Copy requirements.txt into app and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the files to /app working dir
COPY . .

# Run executable on first startup
CMD ["python", "send_requestLLM.py"]