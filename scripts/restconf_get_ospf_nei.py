import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

routers = ["192.168.255.20", "192.168.255.21"]
auth = ("cisco", "cisco")
headers = {"Accept": "application/yang-data+json"}

# Try the root of the OSPF operational model
url_path = "/restconf/data/Cisco-IOS-XE-ospf-oper:ospf-oper"

for ip in routers:
    url = f"https://{ip}{url_path}"
    response = requests.get(url, headers=headers, auth=auth, verify=False)
    
    print(f"\nRouter {ip} Status: {response.status_code}")
    if response.status_code == 200:
        print("Data found! Here is the top-level structure:")
        print(response.json())
    else:
        print("Model not found. Ensure 'restconf' is enabled and OSPF is configured.")
