"""
Job Application Tracker
Run: python tracker.py
"""

import os
import base64
from pyexpat.errors import messages

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, date
from agent import classify_email

load_dotenv()

# Gmail API scope — read-only is enough
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

CREDENTIALS_FILE = "Credentials.json"
TOKEN_FILE = "token.json"


def get_gmail_service():
    """Authenticate and return a Gmail API service object."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"❌  {CREDENTIALS_FILE} not found.")
                print("    Download it from Google Cloud Console → APIs & Services → Credentials.")
                raise SystemExit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_header(headers, name):
    """Extract a header value by name from a list of header dicts."""
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def get_email_body(service, msg_id):
    body = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="full"
    ).execute()
    print("body:" , body)
    body_data=""
    payload = body.get("payload", {})
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    body_data = base64.urlsafe_b64decode(data).decode("utf-8")
                    break
    else:
        data = payload.get("body", {}).get("data", "")
        if data:
            body_data = base64.urlsafe_b64decode(data).decode("utf-8")

    print("body_data:" , body_data)
    return body_data


def fetch_recent_emails(service, max_results=1):
    """
    Fetch up to max_results emails from the last 24 hours.
    Returns a list of dicts with id, subject, sender, snippet.
    """
    import time
    # Gmail 'after' filter uses Unix timestamps (seconds)
    start_time = int(datetime.combine(date.today(), datetime.min.time()).timestamp())
    current_time = int(time.time())
    query = f"after:{start_time} before:{current_time}"

    result = service.users().messages().list(
        userId="me",
        q=query,
        # maxResults=max_results
    ).execute()
    messages = result.get("messages", [])
    if not messages:
        print("No emails found in the last 24 hours.")
        return []

    emails = []
    for msg in messages:
        full = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["Subject", "From", "Date"]
        ).execute()

        headers = full.get("payload", {}).get("headers", [])
        emails.append({
            "id": msg["id"],
            "subject": get_header(headers, "Subject") or "(no subject)",
            "sender":  get_header(headers, "From"),
            "date":    get_header(headers, "Date"),
            "snippet": full.get("snippet", ""),
            "body": get_email_body(service, msg["id"])
        })

    return emails


def print_emails(emails):
    """Print a readable list of emails."""
    print(f"\n{'─'*60}")
    print(f"  {len(emails)} email(s) from the last 24 hours")
    print(f"{'─'*60}")
    for i, e in enumerate(emails, 1):
        print(f"\n[{i}] {e['subject']}")
        print(f"    From:    {e['sender']}")
        print(f"    Date:    {e['date']}")
        print(f"    Snippet: {e['snippet'][:120]}{'...' if len(e['snippet']) > 120 else ''}")
        print(f"    Body:    {e['body']}")
    print(f"\n{'─'*60}")


def main():
    print("🔐 Authenticating with Gmail...")
    service = get_gmail_service()
    print("✅ Authenticated.\n")

    print("📬 Fetching up to 10 emails from the last 24 hours...")
    emails = fetch_recent_emails(service, max_results=10)

    if emails:
        print_emails(emails)

    # for email in emails:
    #     # Get full body if not already fetched
    #     if "body" not in email:
    #         email["body"] = get_email_body(service, email["id"])
    #
    #     email["category"] = classify_email(email)
    #     print(f"Email: {email['subject']} - Category: {email['category']}")


if __name__ == "__main__":
    main()
