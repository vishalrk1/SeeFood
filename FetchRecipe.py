import requests
import json

url = "https://yummly2.p.rapidapi.com/feeds/auto-complete"

querystring = {"q":"chicken soup"}

headers = {
    'x-rapidapi-host': "yummly2.p.rapidapi.com",
    'x-rapidapi-key': "f6f6823b91msh9e92fed91d5356ap136f5djsn494d8f582fb3"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
json_data = json.loads(response.text)

print(json_data)