from celery import shared_task
from .models import SnapshotSchedule
import urllib3
import json
import requests
from .creds_handler import decrypt_text

#@shared_task(bind=True)
#def take_snapshot(self, uuid, cip, ss_name):
def take_snapshot(uuid, cip, ss_name):
    """
    Task to take a snapshot of a VM using Prism Element credentials.

    Args:
        uuid (str): UUID of the VM.
        cip (str): Cluster IP address.
        ss_name (str): Name of the snapshot.

    Returns:
        requests.Response or None: Response object if successful, None otherwise.
    """
    with open("creds.json", 'r') as file:
        # Load the JSON data
        data = json.load(file)

    headers = {"Content-Type": "application/json", "charset": "utf-8"}
    endpoint = "https://{}:9440/PrismGateway/services/rest/v2.0/snapshots/".format(cip)

    try:
        user = decrypt_text(data["username"])
        passw = decrypt_text(data["password"])
    except Exception:
        return None
    

    #print(user,passw)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    #snapshot_name = "snapshot-by-script"
    body = {
        "snapshot_specs": [
            {
                "snapshot_name": ss_name,
                "vm_uuid": uuid
            }
        ]
    }
    print("Trying to take snapshot")
    response = requests.post(endpoint, auth=(user, passw), headers=headers, verify=False, data=json.dumps(body))
    if response.status_code == 201:
        print("snapshot success")
        return response
    else:
        print("snapshot failed")
        return None
