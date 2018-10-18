import os

from pathlib import Path

from smtplib import SMTP
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

from dotenv import find_dotenv, load_dotenv


def create_smtp_connection(server, port, user, password):
    """ Returns smtp object initialised with arguments.
    """
    smtp = SMTP()
    smtp.connect(server, port)
    smtp.starttls()
    smtp.login(user, password)
    return smtp


class Emailer(object):
    """ Object to send emails using MIME.
    """

    def __init__(self, send_from):
        """ Constructor; loads environmental variables.
        """
        load_dotenv(find_dotenv())
        self.send_from = send_from

    def send_mail_with_attachment(self,
                                  recipients,
                                  subject,
                                  text,
                                  attachment_path,
                                  filename):
        """ Create and send email.
        """
        if isinstance(recipients, str):
            recipients = recipients.split(",")
        elif not isinstance(recipients, list):
            raise TypeError("recipients must be list or string")

        msg = MIMEMultipart()
        msg["From"] = self.send_from
        msg["To"] = COMMASPACE.join(recipients)
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = subject
        msg.attach(MIMEText(text))

        with open(attachment_path, "rb") as attachment_file:
            attachment = MIMEApplication(attachment_file.read(), Name=filename)

        attachment["Content-Disposition"] = \
            'attachment; filename="{0}"'.format(filename)
        msg.attach(attachment)

        with self.connection as smtp:
            smtp.sendmail(self.send_from, recipients, msg.as_string())

    @property
    def connection(self):
        """ Returns connection to AWS server.
        """
        server = os.environ.get("SERVER")
        port = os.environ.get("PORT")
        user = os.environ.get("UID")
        password = os.environ.get("PWD")
        return create_smtp_connection(server, port, user, password)
