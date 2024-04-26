import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Email configuration
smtp_server = "mailrelay.corp.nutanix.com"
smtp_port = 25
sender_email = "script_ss@nutanix.com"
recipient_emails = ["rushabh.jain@nutanix.com"]

def send_email(vm_name, cluster_name):
    subject = "Info : Snapshot Taken"
    message = f"""\
    <html>
      <body>
      <br>
	<p>Snapshot was taken successfully.</p> 
    <ul>
      <li>VM Name: {vm_name}</li>
      <li>Cluster Name: {cluster_name}</li>
    </ul>
    <br>
      </body>
    </html>
    """

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            for recipient_email in recipient_emails:
                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["Subject"] = subject
                msg["To"] = recipient_email
            
                # Attach HTML message
                msg.attach(MIMEText(message, "html"))

                # Attach photo as inline im
                server.sendmail(sender_email, recipient_email, msg.as_string())
                print(f"Email sent to {recipient_email}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
#send_email("John", "path/to/photo.jpg")
