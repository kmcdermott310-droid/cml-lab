import requests
from requests.auth import HTTPBasicAuth

#1 Hide the SSL certificate warning messages from the terminal output
requests.packages.urllib3.disable_warnings()

#2 Set the address for the Catalyst Center authentication service
url = "https://sandboxdnac2.cisco.com/dna/system/api/v1/auth/token"

#3 Send a POST request with the username and password to get access
response = requests.post(url, auth=HTTPBasicAuth('devnetuser', 'Cisco123!'), verify=False)

#4 Extract the specific 'Token' string from the JSON data sent back by the server
token = response.json()['Token']

#5 Display a header and the long character string used for future requests
print("JSON Web Token")
print(token)


#Note: This script pulls the JWT from Catalyst Center/DNAC. When I made this, only dnac2 was working I guess I dont know. 
