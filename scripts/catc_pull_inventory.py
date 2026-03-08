import requests
#1 Import the function tool from your JWT pull script
from catc_jwt_pull import get_auth_token

#2 Hide SSL warnings
requests.packages.urllib3.disable_warnings()

#3 EXECUTE the function using () to store the actual string in 'token'
token = get_auth_token()

#4 Define the inventory URL and headers
url = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/network-device"
headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}

#5 Send the GET request
response = requests.get(url, headers=headers, verify=False)

#6 Print the results
print("Connection Successful. Device Data:")
print(response.json())
