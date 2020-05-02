

import os,imghdr
import smtplib
from email.message import  EmailMessage
import pytz
from email.mime.text import MIMEText
from email.mime.base import MIMEBase


GMAIL_DOMAIN = 'smtp.gmail.com'
PORT = 587
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')




class SMTPMailer:
    """
    smtp mailer
    """
    def __init__(self,sender,receivers,subject,body):
        self.msg = EmailMessage()
        self.msg['From'] = sender
        self.msg['To'] = ", ".join(receivers)
        self.msg['Subject'] = subject
        self.msg.set_content(body)

    def add_attachments(self, mail_attachment):
        for attachment in mail_attachment:
            with open(attachment,'rb') as i:
                file_data = i.read()
                ## check if its image..
                file_type = imghdr.what(i.name)
                file_name = i.name
                if file_type is None:
                    self.msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=(file_name.split(os.sep)[-1]))
                else:
                    self.msg.add_attachment(file_data, maintype='image', subtype=imghdr.what(i.name), filename=(file_name.split(os.sep)[-1]))

    def send_mail(self):
        try:
            smtp = smtplib.SMTP_SSL(GMAIL_DOMAIN, 465)
            smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
            smtp.send_message(self.msg)
            print("Mail has been sent")
        except Exception as e:
            print("Error in Sending mail.",e)

    def attach_invite(self):
        self.msg.attach(MIMEText("See attachement for Meeting Invite."))
        icspart = MIMEBase('text', 'calendar', **{'method' : 'REQUEST', 'name' : 'invite.ics'})
        icspart.set_payload( open("invite.ics","rb").read() )
        icspart.add_header('Content-Transfer-Encoding', '8bit')
        icspart.add_header('Content-class', 'urn:content-classes:calendarmessage')
        self.msg.attach(icspart)



sender = 'CCC@gmail.com'
receivers = ['YYYm@gmail.com']
subject = 'sub'
body = 'Message'
mailer = SMTPMailer(sender, receivers, subject, body)
docs_path = os.path.join(os.path.abspath(os.getcwd()),'materials')
list_of_materials = [os.path.join(docs_path,x) for x in os.listdir(docs_path) if os.path.isfile(os.path.join(docs_path,x))]
mailer.add_attachments(list_of_materials)
mailer.attach_invite()
mailer.send_mail()