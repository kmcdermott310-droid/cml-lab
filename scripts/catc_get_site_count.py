import requests
#1 Import your token function
from catc_jwt_pull import get_auth_token

#2 Hide SSL warnings
requests.packages.urllib3.disable_warnings()

#3 Get the token
token = get_auth_token()

#4 Set the Issues API address
url = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/site/count"
headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}

#5 Send the GET request
payload = None
response = requests.request('GET', url, headers=headers, data=payload, verify=False)

#6 Print the results
print(response.text.encode('utf8'))


