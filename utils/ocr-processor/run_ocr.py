import os
import pymongo

def dummy_ocr(annotations):
    return ["Gujarati line 1", "Gujarati line 2"]

def main():
    mongo_uri = os.environ["MONGO_URI"]
    client = pymongo.MongoClient(mongo_uri)
    db = client.ocr_pipeline

    job = db.jobs.find_one({"status": "inferenced"})
    if not job:
        raise Exception("No job found in 'inferenced' state.")

    inter = db.intermediate.find_one({"job_id": job["job_id"]})
    ocr_result = dummy_ocr(inter["annotations"])

    db.intermediate.update_one({"job_id": job["job_id"]}, {"$set": {"ocr_text": ocr_result}})
    db.jobs.update_one({"job_id": job["job_id"]}, {"$set": {"status": "ocr_done"}})
    print(f"[OCR] Completed OCR for Job ID: {job['job_id']}")

if __name__ == "__main__":
    main()
