import requests
#1 Import your token function
from catc_jwt_pull import get_auth_token

#2 Hide SSL warnings
requests.packages.urllib3.disable_warnings()

#3 Get the token
token = get_auth_token()

#4 Set the Issues API address
url = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/issues"
headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}

#5 Send the GET request
response = requests.get(url, headers=headers, verify=False)
issues = response.json().get('response', [])

#6 Print the results
print("Current Network Issues")
print("-" * 20)

for issue in issues:
    name = issue.get('name', 'General Issue')
    severity = issue.get('severity', 'N/A')
    print(f"[{severity}] {name}")
