import requests 
from django.conf import settings


def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v20.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
    "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
    "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": text
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()