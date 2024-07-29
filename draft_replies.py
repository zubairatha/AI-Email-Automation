import datetime
import email
import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from email.message import Message
import requests
import json
from dotenv import find_dotenv, load_dotenv
import os
load_dotenv(find_dotenv())

EMAIL_ACCOUNT = "zubairatha.media@gmail.com"
PASSWORD = os.environ.get("EMAIL_PASSWORD")
# Function to create draft
def create_draft(to, subject, body):
    with imaplib.IMAP4_SSL(host="imap.gmail.com", port=imaplib.IMAP4_SSL_PORT) as imap_ssl:
        print("Logging into mailbox...")
        resp_code, response = imap_ssl.login(EMAIL_ACCOUNT, PASSWORD)

        # Create message
        message = Message()
        message["From"] = EMAIL_ACCOUNT
        message["To"] = to
        message["Subject"] = subject
        message.set_payload(body)
        utf8_message = str(message).encode("utf-8")
        
        # Send message
        imap_ssl.append("[Gmail]/Drafts", '', imaplib.Time2Internaldate(time.time()), utf8_message)

# Connect to mailbox
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL_ACCOUNT, PASSWORD)
mail.select('inbox')

# Calculate date 2 days ago
two_days_ago = datetime.datetime.now() - datetime.timedelta(days=2)
two_days_ago_str = two_days_ago.strftime('%d-%b-%Y')

# Search for unseen emails from the past 2 days
result, data = mail.uid('search', None, '(UNSEEN)', '(SINCE {0})'.format(two_days_ago_str))
email_uids = data[0].split()
i=0
for uid in email_uids:
    result, email_data = mail.uid('fetch', uid, '(RFC822)')
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    for part in email_message.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True)
            body = body.decode('utf-8')
            # Extract sender's email
            sender_email = email_message['From']

            # Create reply message
            reply = MIMEMultipart()
            reply['From'] = EMAIL_ACCOUNT
            reply['To'] = sender_email
            reply['Subject'] = "Re: " + email_message['Subject']

            print()
            # Get reply from RAG
            print(i)
            i+=1
            response = requests.post('https://api-d7b62b.stack.tryrelevance.com/latest/studios/5b3a681c-1262-4946-9891-3fc6fce08e9f/trigger_limited', 
  headers={"Content-Type":"application/json"},
  data=json.dumps({"params":{"client_email":f"{body}"},"project":"8f55a09f8823-41bd-ac6b-747b5b8d3cb3"})
)
            response_dict = json.loads(response.content)

            # Access the 'answer' key
            reply_text = response_dict['output']['answer']
            # Add body to the reply
            reply.attach(MIMEText(reply_text, 'plain'))

            # Convert reply to string
            reply_str = reply.as_string()

            # Create draft instead of sending immediate reply
            create_draft(sender_email, reply['Subject'], reply_text)
            
            print("Draft created in response to:", sender_email)
        else:
            continue

mail.logout()
