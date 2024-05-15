import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Email configuration
smtp_server = "mailrelay.corp.nutanix.com"
smtp_port = 25
sender_email = "script_ss@nutanix.com"
recipient_emails = ["rushabh.jain@nutanix.com"]

def send_email(vm_name, cluster_name,ss_name):
    subject = "Info : Snapshot Success"
    message = f"""\
<html>
  <body>
    <br>
    <p>Snapshot for the below VM was taken successfully.</p> 
    <table border="1" cellspacing="10" cellpadding="10">
      
      <tr>
        <td>VM Name:</td>
        <td>{vm_name}</td>
      </tr>
      <tr>
        <td>Snapshot Name:</td>
        <td>{ss_name}</td>
      </tr>
      <tr>
        <td>Cluster Name:</td>
        <td>{cluster_name}</td>
      </tr>
    </table>
    <br>
  </body>

  <footer>This email was auto-generated by the Snapshot Scheduler Application</footer>
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
