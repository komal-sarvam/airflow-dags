import os
from pymongo import MongoClient

def main():
    mongo_uri = os.environ.get("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client['ocr']
    print("[INFO] Running YOLO inference on files from MongoDB...")
    # Dummy code for now
    print("[SUCCESS] YOLO complete")

if __name__ == "__main__":
    main()
