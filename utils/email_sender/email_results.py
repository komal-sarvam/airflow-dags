import os
import pymongo
import smtplib
from email.message import EmailMessage

def send_email(to_email, content):
    msg = EmailMessage()
    msg.set_content("\n".join(content))
    msg["Subject"] = "Gujarati OCR Results"
    msg["From"] = "ocr@yourdomain.com"
    msg["To"] = to_email

    smtp_host = "smtp.sendgrid.net"
    smtp_user = "apikey"
    smtp_pass = os.environ["EMAIL_API_KEY"]

    with smtplib.SMTP(smtp_host, 587) as smtp:
        smtp.starttls()
        smtp.login(smtp_user, smtp_pass)
        smtp.send_message(msg)

def main():
    mongo_uri = os.environ["MONGO_URI"]
    client = pymongo.MongoClient(mongo_uri)
    db = client.ocr_pipeline

    job = db.jobs.find_one({"status": "llm_done"})
    result = db.intermediate.find_one({"job_id": job["job_id"]})

    send_email("user@example.com", result["llm_text"])
    db.jobs.update_one({"job_id": job["job_id"]}, {"$set": {"status": "emailed"}})

    print(f"[EMAIL] Sent results for Job ID: {job['job_id']}")

if __name__ == "__main__":
    main()
