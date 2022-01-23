import mimetypes
import smtplib
from datetime import date
from email.message import EmailMessage

# Create message and set text content
msg = EmailMessage()
msg['Subject'] = "Job Scraper Results For " + str(date.today())
msg['From'] = 'jobscraperservice@gmail.com'
msg['To'] = 'ediephil@gmail.com'

# Set text content
msg.set_content('Please see attached file')


def attach_file_to_email(email, filename):
    """Attach a file identified by filename, to an email message"""
    with open(filename, 'rb') as fp:
        file_data = fp.read()
        maintype, _, subtype = (mimetypes.guess_type(filename)[0] or 'application/octet-stream').partition("/")
        email.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)


# Attach files
attach_file_to_email(msg, "job-data.xlsx")


def send_mail_smtp(mail, host, username, password):
    s = smtplib.SMTP(host)
    s.starttls()
    s.login(username, password)
    s.send_message(msg)
    s.quit()


send_mail_smtp(msg, 'smtp.gmail.com', 'jobscraperservice@gmail.com', 'gukfctrdybuytenr')
