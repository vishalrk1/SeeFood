import requests
import json
import random

API_KEY = '16b65f6510e040528021ce8f8b439002'

def fetchRecipeData(foodName, apiKey = API_KEY):
    recipe = {}
    
    # Fetching recipe Details from food name
    url = f"https://api.spoonacular.com/recipes/search?query={foodName}&apiKey={apiKey}"
    response = requests.get(url)
    json_data = response.json()
    
    # saving responce code 
    response_status_code = response.status_code
    
    # selecting random recipe from fetched recipes
    recipe_list = json_data['results']
    foodRecipe = random.choice(recipe_list)
    
    recipe_ID = foodRecipe['id']
    
    # getting recipe details from api using recipe id
    url = f"https://api.spoonacular.com/recipes/{recipe_ID}/information?apiKey={apiKey}&includeNutrition=true"
    recipe_response = requests.get(url)
    all_recipe_json_data = recipe_response.json()
    
    # recipe instructions
    recipe_instructions = preprocessing_instructions(all_recipe_json_data['instructions'])
    
    # recipe summary
    recipe_summary = all_recipe_json_data['summary']
    
    # recipe ingredients
    recipe_Ingredients = all_recipe_json_data['extendedIngredients']
    for i, dict in enumerate(recipe_Ingredients):
        recipe_Ingredients[i] = dict['originalString']
    Ingredients = ', '.join(recipe_Ingredients)

    # caloric Breakdow of recipe
    recipe_caloric_breakdown = all_recipe_json_data['nutrition']['caloricBreakdown']
    
    # storing all values in recipe dict
    recipe['id'] = recipe_ID
    recipe['title'] = foodRecipe['title']
    recipe['readyTime'] = foodRecipe['readyInMinutes']
    recipe['soureUrl'] = foodRecipe['sourceUrl']

    recipe['instructions'] = recipe_instructions
    
    recipe['ingridents'] = recipe_Ingredients

    recipe_summary = recipe_summary.replace('<b>', '')
    recipe_summary = recipe_summary.replace('</b>', '')
    recipe['summary'] = recipe_summary

    recipe['percentProtein'] = recipe_caloric_breakdown['percentProtein']
    recipe['percentFat'] = recipe_caloric_breakdown['percentFat']
    recipe['percentCarbs'] = recipe_caloric_breakdown['percentCarbs']
    
    return response_status_code, recipe


def preprocessing_instructions(text):
    word_to_remove = ['<ol>', '</ol>', '<li>', '</li>']
    for word in word_to_remove:
        text = text.replace(word, '')
    return text