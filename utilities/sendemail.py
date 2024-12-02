import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, receiver_email, subject, body, password):
    
    # Create the MIME message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    server=None
    try:
        # Connect to the SMTP server (using Gmail as an example)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        
        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        
        return "Email sent successfully"
    except Exception as e:
        return f"Error: {e}"
    finally:
        server.quit()

# Example usage
sender_email = "akash07may@gmail.com"
receiver_email = "rocktheway.2akash@gmail.com"
subject = "Test Email"
body = "This is a test email sent from Python."
password = ""

print(send_email(sender_email, receiver_email, subject, body, password))
