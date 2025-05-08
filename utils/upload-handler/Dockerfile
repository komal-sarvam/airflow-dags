FROM python:3.10-slim
WORKDIR /app
COPY upload_and_store.py .
RUN pip install pymongo
CMD ["python", "upload_and_store.py"]
