import requests
from requests.auth import HTTPBasicAuth

#1 Hide the SSL certificate warning messages
requests.packages.urllib3.disable_warnings()

#2 Create a function that other scripts can run
def get_auth_token():
    url = "https://sandboxdnac2.cisco.com/dna/system/api/v1/auth/token"
    #3 Send the POST request
    response = requests.post(url, auth=HTTPBasicAuth('devnetuser', 'Cisco123!'), verify=False)
    #4 Return only the token string to the caller
    return response.json()['Token']

#5 This part only runs if you execute THIS file directly
if __name__ == "__main__":
    print(get_auth_token())


#Note: This script pulls the JWT from Catalyst Center/DNAC. When I made this, only dnac2 was working I guess I dont know. This script also acts as a function and can be called from other scripts to auto pull a token.
