import os
import pymongo
from uuid import uuid4

def main():
    mongo_uri = os.environ["MONGO_URI"]
    bucket_name = os.environ["BUCKET_NAME"]

    client = pymongo.MongoClient(mongo_uri)
    db = client.ocr_pipeline

    job_id = str(uuid4())
    db.jobs.insert_one({
        "job_id": job_id,
        "status": "uploaded",
        "filename": "sample.pdf",
        "bucket": bucket_name
    })
    print(f"[UPLOAD] Job created with ID: {job_id}")

if __name__ == "__main__":
    main()
