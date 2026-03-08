import requests
import urllib3

# Suppress the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Try the simplified top-level data path
url = "https://192.168.255.20/restconf/data"

headers = {
    "Accept": "application/yang-data+json"
}

auth = ("cisco", "cisco")

response = requests.get(url, headers=headers, auth=auth, verify=False)

if response.status_code == 200:
    print("Success! Root data found.")
    print(response.json())
else:
    print(f"Failed with Status: {response.status_code}")
