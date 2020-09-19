from email.mime.text import MIMEText
import smtplib

def send_email(email, height, average_height, count):
    from_email = "maqahad1993@gmail.com"
    from_password = "addimaq12345"
    to_email = email
    
    subject = "Height Data"
    message = "Hi, your height is <strong>%s</strong>. Average height from all the people who have registered is <strong>%s</strong>. It is calculated out of <strong>%s</strong> people." %(height, average_height, count)
    
    msg = MIMEText(message,"html")
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)

