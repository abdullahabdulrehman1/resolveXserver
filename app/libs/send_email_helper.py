from mailjet_rest import Client
from flask import current_app

def send_email(to_email, subject, text_content, html_content=None):
    api_key = current_app.config['MAILJET_API_KEY']
    api_secret = current_app.config['MAILJET_API_SECRET']
    sender = current_app.config['MAILJET_SENDER']

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender,
                    "Name": "ResolveX"
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": "Recipient Name"
                    }
                ],
                "Subject": subject,
                "TextPart": f"{text_content}\n\nBest regards,\nThe ResolveX Team",
                "HTMLPart": html_content or f"<p>{text_content}</p><p>Best regards,<br>The ResolveX Team</p>",
                "CustomID": "ResolveXEmail"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code, result.json()