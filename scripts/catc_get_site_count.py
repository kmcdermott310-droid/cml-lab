import requests

url = "/dna/intent/api/v1/site/count"

payload = None

headers = { "Accept": "application/json" }

response = requests.request('GET', url, headers=headers, data = payload)

print(response.text.encode('utf8'))

