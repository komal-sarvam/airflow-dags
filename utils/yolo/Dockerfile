FROM python:3.10-slim

WORKDIR /app
COPY yolo_inference.py .

RUN pip install pymongo

CMD ["python", "yolo_inference.py"]

