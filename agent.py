import os
import anthropic

def classify_email(email_data):
    """Send email to Claude for categorization."""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""
       Analyze this email and categorize it as either "job_application" or "other".
       
       Email Subject: {email_data['subject']}
       Email Body: {email_data['body']}  # Limit body length
       
       Respond with only one word: "job_application" or "other".
       """

    response = client.messages.create(
        model="claude-3-haiku-20240307",  # Use appropriate model
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}]
    )

    category = response.content[0].text.strip().lower()
    return "job_application" if "job_application" in category else "other"