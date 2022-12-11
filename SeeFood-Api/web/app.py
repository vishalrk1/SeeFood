from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from utils import load_prepare_image_torch, create_torch_model, model_pred_torch
from PIL import Image
import requests
import json
import shutil
import numpy as np

import sys
sys.path.insert(1, 'Api Data')
from RecipeData import fetchRecipeData

app = Flask(__name__)
api = Api(app)

# functio  to check correct image url
def check_url(img_url):
    url_lst = img_url.split('.')
    if url_lst[-1] in ['jpg', 'png', 'jpeg']:
        return True
    return False

# Function to return Json
def make_retJson(statusCode, msg):
    retJson = {
        'status': statusCode,
        'msg': msg,
    }
    return retJson


class ImageClassifier(Resource):
    def post(self):
        
        postedData = request.get_json()
        url = postedData['url']
        
        if check_url(url) == False:
            return jsonify(make_retJson(301, 'Invalid Image Url'))
            
        loaded_image = Image.open(requests.get(url, stream=True).raw)
        model, transform = create_torch_model('seeFoodModel_rexnet.pt')
        input_image = load_prepare_image_torch(loaded_image, transform)
        food_name = model_pred_torch(model, input_image)
        responce_status_code, food_details = fetchRecipeData(food_name)
        
        if responce_status_code == 200:
            retJson = {
                "status": responce_status_code,
                "foodName": food_name,
                "foodDetails": food_details,
            }
        else:
            retJson = {
                "status": responce_status_code,
                "foodName": food_name,
            }
            
        return jsonify(retJson)

api.add_resource(ImageClassifier, '/classify')

if __name__ == '__main__':
    app.run(debug=True)