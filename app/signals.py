import requests
import json
from blinker import Namespace
auth_signals = Namespace()
from config import Config
from jinja2 import Template
from app import verification_serializer
from app import reset_serializer
from app import postmark
from flask import current_app
import os

send_verification_code = auth_signals.signal("user-created")
send_reset_password = auth_signals.signal("reset-password")

def load_template(template_name):
    template_path = os.path.join(
        current_app.root_path,
        "templates",
        template_name
    )
    with open(template_path, "r") as f:
        return f.read()

# Handler for the signal
@send_verification_code.connect
def send_verification_code_handler(sender, **kwargs):

    html = load_template("verify_email_template.html")
    text = load_template("verify_email_template.txt")

    values = {
    "name": sender.username,
    "action_url": Config.FRONTEND+"/verify/"+verification_serializer.dumps(sender.username),
    "support_email": Config.SUPPORT_EMAIL,
    }
    html_template = Template(html)
    final_html = html_template.render(**values)
    text_template = Template(text)
    final_text = text_template.render(**values)

    response = postmark.emails.send(
    From=Config.POSTMARK_SENDING_EMAIL,
    To=sender.username,
    Subject="Validate your account on Goat",
    HtmlBody=final_html,
    TextBody=final_text
    )

@send_reset_password.connect
def send_reset_password_email(sender, **kwargs):
    html = load_template("reset_password_template.html")
    text = load_template("reset_password_template.txt")

    values = {
    "name": sender.username,
    "action_url": Config.FRONTEND+"/reset/"+reset_serializer.dumps((sender.username, reset_serializer.dumps(sender.username, salt=sender.password_hash))),
    "support_email": Config.SUPPORT_EMAIL,
    }
    html_template = Template(html)
    final_html = html_template.render(**values)
    text_template = Template(text)
    final_text = text_template.render(**values)
    print(values['action_url'])
    # response = postmark.emails.send(
    # From=Config.POSTMARK_SENDING_EMAIL,
    # To=sender.username,
    # Subject="Reset your password for Goat",
    # HtmlBody=final_html,
    # TextBody=final_text
    # )