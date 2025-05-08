FROM python:3.10-slim
WORKDIR /app
COPY llm_correct.py .
RUN pip install pymongo
CMD ["python", "llm_correct.py"]
