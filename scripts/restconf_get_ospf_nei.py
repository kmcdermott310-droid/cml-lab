import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

routers = ["192.168.255.20", "192.168.255.21"]
auth = ("cisco", "cisco")
headers = {"Accept": "application/yang-data+json"}

# List of common paths for OSPF neighbors
paths = [
    "/restconf/data/Cisco-IOS-XE-ospf-oper:ospf-oper/ospf-state",
    "/restconf/data/ietf-routing:routing-state/control-plane-protocols/control-plane-protocol=ospf,1/ospf:ospf/neighbors",
    "/restconf/data/Cisco-IOS-XE-native:native/router/ospf" # Config path (backup)
]

for ip in routers:
    print(f"\n--- Testing Router {ip} ---")
    for path in paths:
        url = f"https://{ip}{path}"
        try:
            r = requests.get(url, headers=headers, auth=auth, verify=False, timeout=5)
            if r.status_code == 200:
                print(f"[SUCCESS] Path found: {path}")
                # Print a snippet of the data to verify
                print(json.dumps(r.json(), indent=2)[:500] + "...")
                break
            else:
                print(f"[FAIL] {r.status_code} on {path}")
        except Exception as e:
            print(f"[ERROR] Could not connect: {e}")
