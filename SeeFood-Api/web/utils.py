import numpy as np
import torch 
import torch.nn as nn

import torchvision
from torchvision import transforms, datasets, models
from torch.utils.data import Dataset
import timm
import requests
import json

import PIL
import PIL.Image as pil_image

# ------------------------------- ALL FOOD CLASSES -----------------------------------------------------
# ------------------------------------------------------------------------------------------------------

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

# ------------------------------- PYTORCH FUNCTIONS ----------------------------------------------------
# ------------------------------------------------------------------------------------------------------

class seeFoodModel(nn.Module):
    def __init__(self, classes, training=False):
        super(seeFoodModel, self).__init__()
        self.classes = classes
        self.base_model = timm.create_model('rexnet_200',pretrained=True)
        self.base_model.head.fc = nn.Linear(2560, self.classes)
        
    def forward(self, x):
        x = self.base_model(x)
        return x
    
    
def create_torch_model(model_weight_path):
    model = seeFoodModel(classes=101)
    model.load_state_dict(torch.load(model_weight_path))
    
    normalize = transforms.Normalize(
        [0.485, 0.456, 0.406], 
        [0.229, 0.224, 0.225]
    )
    image_transform = transforms.Compose([
        transforms.Resize((300, 300)),
        transforms.CenterCrop(299),
        transforms.ToTensor(),
        normalize,
    ])
    
    return model, image_transform

def load_prepare_image_torch(image, transform):
    # with pil_image.open(filepath) as img:
    img = transform(image)
    img = torch.unsqueeze(img, dim=0)
    return img

def model_pred_torch(model, image, class_names=classes):
    model.eval()
    pred = model(image)
    pred = torch.softmax(pred, dim=1).argmax(dim=1).squeeze()
    food_name = class_names[pred]
    return food_name


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
