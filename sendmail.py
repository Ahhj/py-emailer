import os
import re
import zipfile
import smtplib
import sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders


"""
	Required Input:
		- Source folder (src)
		- Archive name (dst)
		- SMTP information
		- Recipient email
"""
DIRECTORY_OF_IMAGES = "D:\Flat-UI-master\images\demo"
NAME_OF_DESTINATION_ARCHIVE = "test" # test.zip
SUBJECT = "Test Images Zipped"
RECIPIENTS = "fake@gmail.com, fake+other@gmail.com" #separated by comma

server = "smtp.gmail.com"
port = 587
username = "fake@gmail.com"
password = "fake"
sender = username
isGMAIL = True

# From http://stackoverflow.com/questions/14568647/create-zip-in-python
def zip(src, dst):
	zf = zipfile.ZipFile("%s.zip" % (dst), "w")
	src = os.path.abspath(src)
	for d, s, f in os.walk(src):
		for n in f:
			if re.match(r"^.*[.](png|jpg|gif|jpeg)$", n):
				abs_name = os.path.abspath(os.path.join(d,n))
				arc_name = abs_name[len(src) + 1:]
				zf.write(abs_name, arc_name)
	zf.close()


# From http://stackoverflow.com/questions/3362600/how-to-send-email-attachments-with-python

def sendMsg():
	msg = MIMEMultipart()
	msg['Subject'] = SUBJECT
	msg['From'] = sender
	msg['To'] = RECIPIENTS

	part = MIMEBase("application", "octet-stream")
	part.set_payload(open(NAME_OF_DESTINATION_ARCHIVE + ".zip", "rb").read())
	Encoders.encode_base64(part)
	part.add_header("Content-Disposition", "attachment; filename=\"%s.zip\"" % (NAME_OF_DESTINATION_ARCHIVE))
	msg.attach(part)

	smtp = smtplib.SMTP(server, port)
	if isGMAIL:
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()
	smtp.login(username,password)
	smtp.sendmail(sender, RECIPIENTS, msg.as_string())
	smtp.close()

zip(DIRECTORY_OF_IMAGES, NAME_OF_DESTINATION_ARCHIVE)

try:
	sendMsg()
except Exception, exc:
    sys.exit( "mail failed; %s" % str(exc) )