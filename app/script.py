import requests
import urllib3
import json
from pathlib import Path
from requests.auth import HTTPBasicAuth
import csv
from datetime import datetime
from .creds_handler import encrypt_text, decrypt_text
def get_vms_form_pe(uuid, ip, name):
    """
    Fetches VMs from a Prism Element (PE) cluster.
    
    Args:
        uuid (str): The UUID of the PE cluster.
        ip (str): The IP address of the PE cluster.
        name (str): The name of the PE cluster.
    
    Returns:
        list: A list of dictionaries containing VM information.
    """
    with open("creds.json", 'r') as file:
        creds_data = json.load(file)

    data = []
    headers = {"Content-Type": "application/json", "charset": "utf-8"}
    count = 0
    cluster_name = name
    Pe_IP = ip
    try:
        user = decrypt_text(creds_data["username"])
        passw = decrypt_text(creds_data["password"])
    except Exception:
        return None
    #print(user, passw)
    endpoint = "https://{}:9440/PrismGateway/services/rest/v2.0/vms/".format(Pe_IP)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(endpoint, auth=(user, passw), headers=headers, verify=False)
    
    if response.status_code != 200:
        print("Error in getting VMs for PE:", Pe_IP)
        return None

    for obj in response.json()["entities"]:
        item = {
            "vm_name": obj["name"],
            "uuid": obj["uuid"],
            "cip": Pe_IP,
            "cluster_name": cluster_name
        }
        data.append(item)
        count += 1

    print("TOTAL VMS FETCHED:", count)

    data = sorted(data, key=lambda x: x.get('vm_name', ''))
    return data


#this script has GUI 
def get_pe(creds):
    """
    Fetches Prism Element (PE) clusters from Prism Central (PC) and saves the data in a JSON file.

    Args:
        creds (list): List containing PC credentials [PC_IP, username, password].

    Returns:
        int: 1 if successful.
    """
    PC_IP = creds[0]
    user = creds[1]
    passw = creds[2]
    headers = {"Content-Type": "application/json", "charset": "utf-8"}
    endpoint = "https://{}:9440/api/nutanix/v3/groups".format(PC_IP)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    body = {
        "entity_type": "cluster",
        "group_member_attributes": [
            {"attribute": "name"},
            {"attribute": "version"},
            {"attribute": "is_available"},
            {"attribute": "service_list"},
            {"attribute": "full_version"},
            {"attribute": "external_ip_address"}
        ]
    }
    response = requests.post(endpoint, auth=(user, passw), headers=headers, verify=False, data=json.dumps(body))
    if response.status_code != 200:
        return None

    data = []
    n = int(response.json()["total_entity_count"])
    uuid = ""
    c = 0

    for i in range(n):
        uuid = response.json()["group_results"][0]["entity_results"][i]["entity_id"]
        obj = response.json()["group_results"][0]["entity_results"][i]["data"]
        name = ""
        ip = ""
        
        for item in obj:
            if item['name'] == 'name':
                name = item['values'][0]['values'][0]
            if item['name'] == 'external_ip_address':
                ip = item['values'][0]['values'][0]
        
        c = c + 1
        data.append({"index": c, "uuid": uuid, "name": name, "ip": ip})

    with open("pe_list_generated.json", "w") as json_file:
         print("Prism element data fetched from PC and saved in pe_list_generated.json.")
         json.dump(data, json_file, indent=4)

    with open("creds.json", "w") as j:
        obj = {
            "username": encrypt_text(user),
            "password": encrypt_text(passw)
        }
        json.dump(obj, j, indent=4)
        print("Creds saved in creds.json")
        
    return 1



def get_vm_uuidsc(creds):
    """
    Fetches VM UUIDs from Prism Central (PC) and associates them with their respective PE clusters.

    Args:
        creds (list): List containing PC credentials [PC_IP, username, password].

    Returns:
        list: A list of dictionaries containing VM UUIDs associated with their PE clusters.
    """
    with open("pe_list_generated.json", 'r') as file:
        data = json.load(file)

    uuid_ip = {}
    for obj in data:
        uuid_ip[obj["uuid"]] = obj["ip"]

    PC_IP = creds[0]
    user = creds[1]
    passw = creds[2]
    headers = {"Content-Type": "application/json", "charset": "utf-8"}
    endpoint = "https://{}:9440/api/nutanix/v3/vms/list".format(PC_IP)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    vms_uuid = []
    vm_count = 0
    offset = 0
    length = 500

    while True:
        body = {"kind": "vm", "length": length, "offset": offset}
        try:
            response = requests.post(endpoint, auth=(user, passw), headers=headers, verify=False, data=json.dumps(body))
            if response.status_code != 200:
                return None
        except TimeoutError:
            return None

        entities = response.json().get("entities", [])
        if not entities:
            break

        for obj in entities:
            item = {
                "vm_name": obj["status"]["name"],
                "uuid": obj["metadata"]["uuid"],
                "cip": uuid_ip[obj["spec"]["cluster_reference"]["uuid"]]
            }
            vms_uuid.append(item)
            vm_count += 1

        if len(entities) < length:
            break

        offset += length

    obj = {"Vm_count": vm_count}
    vms_uuid.append(obj)

    vms_uuid = sorted(vms_uuid, key=lambda x: x.get('cip', ''))

    with open("pc_generated_vms_uuid.json", "w") as json_file:
        print("VMS data fetched from PC and saved in pc_generated_vms_uuid.json.")
        json.dump(vms_uuid, json_file, indent=4)

    return vms_uuid

#creds = ["10.38.87.39","rushabh","Nutanix/4u"]
#get_pe(creds)
#get_vm_uuidsc(creds)
#take_snapshots(creds)
#get_pe(creds=creds)
#get_vms()
#get_vms_form_pe()