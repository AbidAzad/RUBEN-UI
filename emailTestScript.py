import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
   
fromaddr = "abillou60@gmail.com"
toaddr = "sf668@scarletmail.rutgers.edu"
   
# instance of MIMEMultipart 
msg = MIMEMultipart() 
  
# storing the senders email address   
msg['From'] = fromaddr 
  
# storing the receivers email address  
msg['To'] = toaddr 
  
# storing the subject  
msg['Subject'] = "Python Email Test"
  
# string to store the body of the mail 
body = """
Subject: Test Email

Hello,

This is a test email sent from Python using the smtplib library.

If you can read this, the email was sent successfully!

Best regards,
Abid Azad
"""
# attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain')) 
  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login(fromaddr, "zgki fwts swac cigv") 
  
# Converts the Multipart msg into a string 
text = msg.as_string() 
  
# sending the mail 
s.sendmail(fromaddr, toaddr, text) 
  
# terminating the session 
s.quit() 
