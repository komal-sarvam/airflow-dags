FROM python:3.10-slim
WORKDIR /app
COPY email_results.py .
RUN pip install pymongo
CMD ["python", "email_results.py"]
