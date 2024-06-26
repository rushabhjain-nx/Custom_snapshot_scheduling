import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
smtp_server = "mailrelay.corp.nutanix.com"
smtp_port = 25
sender_email = "script_ss@nutanix.com"
recipient_emails = ["rushabh.jain@nutanix.com"]

def send_email(vm_name, cluster_name, ss_name, message_info):
    """
    Sends an email notification about snapshot execution status.

    Args:
        vm_name (str): The name of the virtual machine.
        cluster_name (str): The name of the cluster.
        ss_name (str): The name of the snapshot.
        message_info (str): The status of the snapshot execution ("success" or "failed").
    """

    if message_info == "success":
        subject = "Info : Snapshot Success"
        message = f"""\
        <html>
          <body>
            <br>
            <p>Snapshot execution for the below VM was successful.</p> 
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
    else:
        subject = "Info : Snapshot Failed"
        message = f"""\
        <html>
          <body>
            <br>
            <p>Snapshot execution for the below VM failed.</p> 
            <table border="1" cellspacing="10" cellpadding="10">
              
              <tr>
                <td>VM Name:</td>
                <td>{vm_name}</td>
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
        # Connect to SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            for recipient_email in recipient_emails:
                # Create MIMEMultipart message
                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["Subject"] = subject
                msg["To"] = recipient_email
            
                # Attach HTML message
                msg.attach(MIMEText(message, "html"))

                # Sending email
                server.sendmail(sender_email, recipient_email, msg.as_string())
                print(f"Email sent to {recipient_email}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
#send_email("John", "path/to/photo.jpg")

#<p> <strong> Next Snapshot Retry will happen after one hour.</strong> <p>