#!/usr/bin/python

"""
Usage:
    python send-email.py content.md attachment.html
"""

import re
import smtplib
import sys

from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

content_fn = sys.argv[1]
attachment_fn = sys.argv[2]

# me == my email address
# you == recipient's email address
me = "me@someemail.com"
you = "you@someemail.com"

print(content_fn)
print(attachment_fn)

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "email send report"
msg['From'] = me
msg['To'] = you

# Process content by making the email body looks good
html = open(content_fn).read()
html = re.sub(r'```python(.*?)```', '', html, flags=re.DOTALL)
html = re.sub(r'^#', '<br/>#', html, flags=re.MULTILINE)
html = re.sub(r'^<div>', '<br/><div>', html, flags=re.MULTILINE)
html = re.sub(r'^    \*\*\*\*\*\*', '<br/>    ******', html, flags=re.MULTILINE)
html = re.sub(r'\*\*\*\*\*\*$', '******<br/>', html, flags=re.MULTILINE)

# print(html)

base_fn = basename(attachment_fn)
with open(attachment_fn, 'rb') as fn:
    part1 = MIMEApplication(fn.read(), Name=base_fn)
# After the file is closed
part1['Content-Disposition'] = 'attachment; filename="%s"' % base_fn
msg.attach(part1)

part2 = MIMEText(html, 'html')
msg.attach(part2)

# Send the message via local SMTP server.
s = smtplib.SMTP('localhost')
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
s.sendmail(me, you, msg.as_string())
s.quit()
