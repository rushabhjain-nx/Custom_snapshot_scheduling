from celery import shared_task
from .models import SnapshotSchedule
import urllib3
import json
import requests


def take_snapshot(uuid,cip):
    with open("creds.json", 'r') as file:
    # Load the JSON data
        data = json.load(file)
    #print(data)
    headers = {"Content-Type": "application/json", "charset": "utf-8"}
    endpoint = "https://{}:9440/PrismGateway/services/rest/v2.0/snapshots/".format(cip)

    user=data["username"]
    passw = data["password"]
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    snapshot_name = "snapshot-by-script"
    body = {
        "snapshot_specs":[
            {
                "snapshot_name":snapshot_name,
                "vm_uuid":uuid

            }
        ]
    }
    print("Trying to take snapshot")
    response = requests.post(endpoint,auth=(user, passw),headers=headers,verify=False,data=json.dumps(body))
    if response.status_code == 201:
                print("snapshot success")
                return response
    else:
                print("snapshot failed")
                return None
    #response = requests.post(endpoint,auth=(user, passw),headers=headers,verify=False,data=json.dumps(body))

           
            

