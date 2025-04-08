from fastapi import FastAPI, BackgroundTasks
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
import boto3
import email
import imaplib
import json
import openai
import os
import psycopg2
import time

app = FastAPI()
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
DB_URL = os.getenv("DATABASE_URL")
IMAP_HOST = os.getenv("IMAP_HOST")
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASS = os.getenv("IMAP_PASS")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


openai.api_key = OPENAI_API_KEY
sqs = boto3.client("sqs", region_name=AWS_REGION)
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()


class EmailPayload(BaseModel):
    sender: str
    subject: str
    body: str
    message_id: Optional[str] = None


def enqueue_email(payload: EmailPayload):
    sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=payload.json()
    )

@app.post("/ingest-emails")
def ingest_email(payload: EmailPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(enqueue_email, payload)
    return {"status": "queued"}

def fetch_emails():
    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(IMAP_USER, IMAP_PASS)
    mail.select("inbox")
    _, messages = mail.search(None, "UNSEEN")
    for num in messages[0].split():
        _, data = mail.fetch(num, '(RFC822)')
        raw = email.message_from_bytes(data[0][1])
        subject = raw['subject']
        sender = raw['from']
        body = ""
        if raw.is_multipart():
            for part in raw.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = raw.get_payload(decode=True).decode()

        payload = EmailPayload(sender=sender, subject=subject, body=body)
        enqueue_email(payload)

    mail.logout()

def process_email(payload: EmailPayload):
    prompt = f"""
    Classify and extract the following details from the email:
    - Category
    - Issue Summary
    - Suggested Response

    Email:
    {payload.body}

    Return in JSON format.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message['content']

def consume_from_sqs():
    while True:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=10
        )

        messages = response.get("Messages", [])
        for msg in messages:
            try:
                payload_dict = json.loads(msg["Body"])
                payload = EmailPayload(**payload_dict)

                result = process_email(payload)
                print("Processed Result:", result)

                sqs.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=msg["ReceiptHandle"]
                )
            except Exception as e:
                print("Error processing message:", e)

        time.sleep(1)
