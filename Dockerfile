# Base lightweight image with Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy your code and model files
COPY . /app

# Install OS-level dependencies for OpenCV and inference
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Example requirements.txt:
# torch==2.0.1
# torchvision==0.15.2
# opencv-python
# pymongo

# Run the inference script
CMD ["python", "yolo_inference.py"]
