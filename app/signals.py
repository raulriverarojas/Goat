import requests
import json
from blinker import Namespace
auth_signals = Namespace()
from config import Config


user_created = auth_signals.signal('user-created')

# Handler for the signal
@user_created.connect
def user_created_handler(sender, **kwargs):

    headers = {
            "X-Postmark-Server-Token": Config.POSTMARK_SERVER_TOKEN,
            "Accept": "application/json",
            "Content-Type": "application/json"
            }
    url = "https://api.postmarkapp.com/email"
    email ={
        "From": Config.POSTMARK_SENDING_EMAIL,
        "To": sender.username,
        "Subject": "Validate your account",
        "HtmlBody": "<b>Hello</b>",
        "TextBody": "Hello",
        "Metadata": {
            "Color":"blue",
        },
        "MessageStream": "outbound"
        }
    r = requests.post(url, headers=headers, json=email)
    print(r.status_code)
    print(json.dumps(r.json(), indent=4))
    print(f'User created: {sender.username}')