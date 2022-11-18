import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def alert(main_msg):
   mail_from = 'selvakumar@gcetly.ac.in'
   mail_to = 'msphilip10@gmail.com'
   msg = MIMEMultipart()
   msg['From'] = mail_from
   msg['To'] = mail_to
   msg['Subject'] = '!Alert Mail On Product Shortage! - Regards'
   mail_body = main_msg
   msg.attach(MIMEText(mail_body))
   print(msg)

   try:
      server = smtplib.SMTP_SSL('smtp.sendgrid.net', 465)
      server.ehlo()
      server.login('apikey',os.environ.get('SENDGRID_API_KEY'))
      server.sendmail(mail_from, mail_to, msg.as_string())
      server.close()
      print("Mail sent successfully!")
   except:
      print("Some Issue, Mail not Sent :(")