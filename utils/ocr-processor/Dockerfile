FROM python:3.10-slim
WORKDIR /app
COPY run_ocr.py .
RUN pip install pymongo
CMD ["python", "run_ocr.py"]
