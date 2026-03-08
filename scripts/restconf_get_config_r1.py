import requests
import json

# Replace with your R1 or R2 IP
url = "https://192.168.255.20/restconf/data/Cisco-IOS-XE-native:native"

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# Standard CML credentials
auth = ("cisco", "cisco")

try:
    response = requests.get(url, headers=headers, auth=auth, verify=False)
    
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Failed! Status Code: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Error: {e}")
