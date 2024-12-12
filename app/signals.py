import requests
import json
from blinker import Namespace
auth_signals = Namespace()
from config import Config
from jinja2 import Template
from app import dangerous_serializer
from app import postmark
user_created = auth_signals.signal('user-created')
# Handler for the signal
@user_created.connect
def user_created_handler(sender, **kwargs):

    ### This app uses postmark templates the following template is just for completeness
    html= r"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Welcome to GOAT</title>
    <style>
        @media only screen and (max-width: 620px) {
        table.body-action {
            width: 100% !important;
        }
        .button {
            width: 100% !important;
        }
        }
        
        .button {
        background-color: #3869D4;
        border-top: 10px solid #3869D4;
        border-right: 18px solid #3869D4;
        border-bottom: 10px solid #3869D4;
        border-left: 18px solid #3869D4;
        display: inline-block;
        color: #FFF;
        text-decoration: none;
        border-radius: 3px;
        box-shadow: 0 2px 3px rgba(0, 0, 0, 0.16);
        -webkit-text-size-adjust: none;
        box-sizing: border-box;
        }
        
        .body-sub {
        margin-top: 25px;
        padding-top: 25px;
        border-top: 1px solid #EDEFF2;
        }
        
        .sub {
        font-size: 13px;
        color: #666;
        }
        
        body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.5;
        color: #333;
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
        }
    </style>
    </head>
    <body>
    <!-- Header -->
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 30px;">
        <tr>
        <td align="center">
            <img src="{{company_logo}}" alt="GOAT" width="150">
        </td>
        </tr>
    </table>

    <h1 style="color: #2F3133; text-align: center;">Welcome to GOAT, {{name}}!</h1>
    
    <p>Thanks for joining GOAT! We're excited to have you as part of our community. To get started, please verify your email address by clicking the button below:</p>

    <!-- Action -->
    <table class="body-action" align="center" width="100%" cellpadding="0" cellspacing="0">
        <tr>
        <td align="center">
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
                <td align="center">
                <table border="0" cellspacing="0" cellpadding="0">
                    <tr>
                    <td>
                        <a href="{{action_url}}" class="button" target="_blank">Verify Email Address</a>
                    </td>
                    </tr>
                </table>
                </td>
            </tr>
            </table>
        </td>
        </tr>
    </table>


    <!-- Help -->
    <p style="margin-top: 30px;">If you need any help getting started, reply to this email.</p>

    <!-- Sub copy -->
    <table class="body-sub">
        <tr>
        <td>
            <p class="sub">If you're having trouble with the button above, copy and paste the URL below into your web browser:</p>
            <p class="sub">{{action_url}}</p>
            <p class="sub">This verification link will expire in 24 hours.</p>
        </td>
        </tr>
    </table>

    <!-- Footer -->
    <table class="body-sub" style="margin-top: 25px;">
        <tr>
        <td>
            <p class="sub">
            You're receiving this email because you recently created an account on GOAT. 
            If you didn't request this, please ignore this email or <a href="{{support_email}}">contact support</a>.
            </p>
        </td>
        </tr>
    </table>
    </body>
    </html>
    """
    text=r"""
    Welcome to GOAT, {{name}}!
    Thanks for joining GOAT! We're excited to have you as part of our community. To get started, please verify your email address by visiting this link:
    {{action_url}}
    If you need any help getting started, reply to this email.

    This verification link will expire in 24 hours.

    You're receiving this email because you recently created an account on Goat. If you didn't request this, please ignore this email or contact support at: {{support_url}}
    """
    values = {
    'name': sender.username,
    'action_url': Config.FRONTEND+"/verify/"+dangerous_serializer.dumps(sender.username),
    'support_email': Config.SUPPORT_EMAIL,
    }
    html_template = Template(html)
    final_html = html_template.render(**values)
    text_template = Template(text)
    final_text = text_template.render(**values)

    response = postmark.emails.send(
    From=Config.POSTMARK_SENDING_EMAIL,
    To=sender.username,
    Subject='Validate your account on Goat',
    HtmlBody=final_html,
    TextBody=final_text
    )

    # headers = {
    #         "X-Postmark-Server-Token": Config.POSTMARK_SERVER_TOKEN,
    #         "Accept": "application/json",
    #         "Content-Type": "application/json"
    #         }
    # url = "https://api.postmarkapp.com/email"
    # email ={
    #     "From": Config.POSTMARK_SENDING_EMAIL,
    #     "To": sender.username,
    #     "Subject": "Validate your account",
    #     "HtmlBody": "<b>Hello</b>",
    #     "MessageStream": "outbound"
    #     }
    # r = requests.post(url, headers=headers, json=email)
    # print(r.status_code)
    # print(json.dumps(r.json(), indent=4))
    # print(json.dumps(r))