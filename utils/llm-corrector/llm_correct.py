import os
import pymongo

def llm_fix(text_lines):
    return [line.upper() for line in text_lines]

def main():
    mongo_uri = os.environ["MONGO_URI"]
    client = pymongo.MongoClient(mongo_uri)
    db = client.ocr_pipeline

    job = db.jobs.find_one({"status": "ocr_done"})
    inter = db.intermediate.find_one({"job_id": job["job_id"]})

    corrected = llm_fix(inter["ocr_text"])
    db.intermediate.update_one({"job_id": job["job_id"]}, {"$set": {"llm_text": corrected}})
    db.jobs.update_one({"job_id": job["job_id"]}, {"$set": {"status": "llm_done"}})

    print(f"[LLM] Corrected text for Job ID: {job['job_id']}")

if __name__ == "__main__":
    main()
