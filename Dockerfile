# Use NVIDIA CUDA 11.2 base image
FROM nvidia/cuda:11.2.2-cudnn8-runtime-ubuntu20.04

# Install dependencies and Python 3.10
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.10 python3.10-venv python3.10-dev curl build-essential libffi-dev gcc g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.10 as the default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && update-alternatives --set python3 /usr/bin/python3.10

# Install the latest pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . /app/

# Expose the application port
EXPOSE 9878

# Use Gunicorn for production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9878", "app:app"]
