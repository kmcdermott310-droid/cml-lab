import requests
import urllib3
import json

# Disable SSL warnings for lab environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

routers = ["192.168.255.20", "192.168.255.21"]
auth = ("cisco", "cisco")
headers = {"Accept": "application/yang-data+json"}

# The URL for OSPF operational data
url_path = "/restconf/data/Cisco-IOS-XE-ospf-oper:ospf-oper/ospf-state/ospf-instance"

for ip in routers:
    print(f"\n{'='*20} Checking {ip} {'='*20}")
    url = f"https://{ip}{url_path}"
    
    try:
        response = requests.get(url, headers=headers, auth=auth, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            # Navigate the JSON structure to find neighbor list
            instances = data.get("Cisco-IOS-XE-ospf-oper:ospf-instance", [])
            
            for inst in instances:
                neighbors = inst.get("ospf-area", [{}])[0].get("ospf-interface", [{}])[0].get("ospf-neighbor", [])
                
                if not neighbors:
                    print("No OSPF neighbors found.")
                    continue

                print(f"{'Neighbor ID':<15} {'Address':<15} {'State':<15} {'Interface':<15}")
                for nei in neighbors:
                    print(f"{nei.get('neighbor-id', 'N/A'):<15} "
                          f"{nei.get('address', 'N/A'):<15} "
                          f"{nei.get('state', 'N/A'):<15} "
                          f"{nei.get('if-name', 'N/A'):<15}")
        else:
            print(f"Error: Status {response.status_code}")
            
    except Exception as e:
        print(f"Connection Failed: {e}")
