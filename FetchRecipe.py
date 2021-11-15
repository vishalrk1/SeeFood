# import http.client

# conn = http.client.HTTPSConnection("recipesapi2.p.rapidapi.com")

# headers = {
#     'x-rapidapi-host': "recipesapi2.p.rapidapi.com",
#     'x-rapidapi-key': "f6f6823b91msh9e92fed91d5356ap136f5djsn494d8f582fb3"
#     }

# conn.request("GET", "/recipes/pizza?maxRecipes=1", headers=headers)

# res = conn.getresponse()
# data = res.read()
# Recipe_data = data.decode("utf-8")
# # Recipe_data = ast.literal_eval(Recipe_data)

# print(str(Recipe_data['data']))

import requests
import json

url = "https://recipesapi2.p.rapidapi.com/recipes/pizza"

querystring = {"maxRecipes":"2"}

headers = {
    'x-rapidapi-host': "recipesapi2.p.rapidapi.com",
    'x-rapidapi-key': "f6f6823b91msh9e92fed91d5356ap136f5djsn494d8f582fb3"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
json_data = json.loads(response.text)

# recipes_list = []
# for recipe in json_data['data']:
#     recipes_list.append(recipe)
    
# recipe_data = json_data['data'][0]
 
print(json_data['data'][0])