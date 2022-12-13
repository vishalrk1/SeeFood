import tensorflow as tf
import numpy as np
import torch
import torch.nn as nn
import timm
from torchvision import transforms
import os

import requests
import json

classes = ['apple pie', 'baby back ribs', 'baklava', 'beef carpaccio', 'beef tartare',
 'beet salad', 'beignets', 'bibimbap', 'bread pudding', 'breakfast burrito',
 'bruschetta', 'caesar_salad', 'cannoli', 'caprese salad', 'carrot cake',
 'ceviche', 'cheese plate', 'cheesecake', 'chicken curry',
 'chicken quesadilla', 'chicken wings', 'chocolate cake', 'chocolate mousse',
 'churros', 'clam chowder', 'club sandwich', 'crab cakes', 'creme brulee',
 'croque madame', 'cup cakes', 'deviled eggs', 'donuts', 'dumplings', 'edamame',
 'eggs benedict', 'escargots', 'falafel', 'filet mignon', 'fish and chips',
 'foie gras', 'french fries', 'french onion soup', 'french toast',
 'fried calamari', 'fried rice', 'frozen yogurt', 'garlic bread', 'gnocchi',
 'greek salad', 'grilled cheese sandwich', 'grilled salmon', 'guacamole',
 'gyoza', 'hamburger', 'hot and sour soup', 'hot dog', 'huevos rancheros',
 'hummus', 'ice cream', 'lasagna', 'lobster bisque', 'lobster roll sandwich',
 'macaroni and cheese', 'macarons', 'miso soup', 'mussels', 'nachos',
 'omelette', 'onion rings', 'oysters', 'pad thai', 'paella', 'pancakes',
 'panna cotta', 'peking duck', 'pho', 'pizza', 'pork chop', 'poutine',
 'prime rib', 'pulled pork sandwich', 'ramen', 'ravioli', 'red velvet cake',
 'risotto', 'samosa', 'sashimi', 'scallops', 'seaweed salad',
 'shrimp and grits', 'spaghetti bolognese', 'spaghetti carbonara',
 'spring rolls', 'steak', 'strawberry_shortcake', 'sushi', 'tacos', 'takoyaki',
 'tiramisu', 'tuna tartare', 'waffles']

##########################################################################
#                    TENSORFLOW FUNCTIONS                                #
##########################################################################

def load_prepare_image_tf(filepath, img_size, rescale=False):
    img = tf.io.decode_image(filepath, channels=3)
    img = tf.image.resize(img, img_size)

    if rescale:
        return img/255.
    else:
        return img

def model_pred_tf(model_path, img, class_names=classes):
    # Load TFLite model and allocate tensors.
    interpreter = tf.lite.Interpreter(model_path=model_path)
    #allocate the tensors
    interpreter.allocate_tensors()

    input_tensor= np.array(np.expand_dims(img,0), dtype=np.float32)
    input_index = interpreter.get_input_details()[0]["index"]

    # setting input tensor
    interpreter.set_tensor(input_index, input_tensor)

    #Run the inference
    interpreter.invoke()
    output_details = interpreter.get_output_details()

    # output data of image
    output_data = interpreter.get_tensor(output_details[0]['index'])

    pred = output_data.argmax()

    food_name = class_names[pred]

    return food_name

##########################################################################
#                    PyTorch FUNCTIONS                                   #
##########################################################################

def get_model_pt(model_path):
    model = timm.create_model('vit_base_patch16_224', pretrained=False)
    model.head = nn.Linear(in_features=768, out_features=len(classes), bias=True)
    model.load_state_dict(torch.load('models/ViT-101-1.pt', map_location='cpu'))
    return model

def load_prepare_image_pt(input_image):
    normalize = transforms.Normalize(
        [0.485, 0.456, 0.406], 
        [0.229, 0.224, 0.225]
    )
    img_transform = transforms.Compose([
        transforms.Resize((225, 225)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        normalize,
    ])
    input_image = img_transform(input_image).unsqueeze(0)
    return input_image
    

def model_pred_pt(input_image, model_path):
    model = get_model_pt(model_path)
    probs = model(input_image)
    y_preds = torch.softmax(probs, dim=1).detach().numpy().argmax()
    pred = classes[y_preds]
    return pred

def fetch_recipe(food_name):
    url = "https://recipesapi2.p.rapidapi.com/recipes/"+food_name
    querystring = {"maxRecipes":"1"}

    headers = {
        'x-rapidapi-host': "recipesapi2.p.rapidapi.com",
        'x-rapidapi-key': "f6f6823b91msh9e92fed91d5356ap136f5djsn494d8f582fb3"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_data = json.loads(response.text)

    recipe_data = json_data['data'][0]

    return recipe_data