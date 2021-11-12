import tensorflow as tf
import numpy as np
import os

import requests
import json
# def view_and_predict(target_dir, target_class, model_path):

#     # Reading image and plotting image
#     img = tf.io.read_file(target_folder + '/' + random_image[0])
#     img = tf.io.decode_image(img)
#     img = tf.image.resize(img,(224,224))
#     img_show = img/255.

#     pred = model_pred(model_path, img, class_names)

#     plt.imshow(img_show)
#     plt.title(f"Real Label: {target_class},   prediction: {pred}")
#     plt.axis('off');

#     return img


classes = ['apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare',
 'beet_salad', 'beignets', 'bibimbap', 'bread_pudding', 'breakfast_burrito',
 'bruschetta', 'caesar_salad', 'cannoli', 'caprese_salad', 'carrot_cake',
 'ceviche', 'cheese_plate', 'cheesecake', 'chicken_curry',
 'chicken_quesadilla', 'chicken_wings', 'chocolate_cake', 'chocolate_mousse',
 'churros', 'clam_chowder', 'club_sandwich', 'crab_cakes', 'creme_brulee',
 'croque_madame', 'cup_cakes', 'deviled_eggs', 'donuts', 'dumplings', 'edamame',
 'eggs_benedict', 'escargots', 'falafel', 'filet_mignon', 'fish_and_chips',
 'foie_gras', 'french_fries', 'french_onion_soup', 'french_toast',
 'fried_calamari', 'fried_rice', 'frozen_yogurt', 'garlic_bread', 'gnocchi',
 'greek_salad', 'grilled_cheese_sandwich', 'grilled_salmon', 'guacamole',
 'gyoza', 'hamburger', 'hot_and_sour_soup', 'hot_dog', 'huevos_rancheros',
 'hummus', 'ice_cream', 'lasagna', 'lobster_bisque', 'lobster_roll_sandwich',
 'macaroni_and_cheese', 'macarons', 'miso_soup', 'mussels', 'nachos',
 'omelette', 'onion_rings', 'oysters', 'pad_thai', 'paella', 'pancakes',
 'panna cotta', 'peking_duck', 'pho', 'pizza', 'pork_chop', 'poutine',
 'prime rib', 'pulled pork sandwich', 'ramen', 'ravioli', 'red velvet cake',
 'risotto', 'samosa', 'sashimi', 'scallops', 'seaweed salad',
 'shrimp and grits', 'spaghetti bolognese', 'spaghetti carbonara',
 'spring rolls', 'steak', 'strawberry_shortcake', 'sushi', 'tacos', 'takoyaki',
 'tiramisu', 'tuna_tartare', 'waffles']

def load_prepare_image(filepath, img_size, rescale=False):
    img = tf.io.decode_image(filepath, channels=3)
    img = tf.image.resize(img, img_size)

    if rescale:
        return img/255.
    else:
        return img

def model_pred(model_path, img, class_names=classes):
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

def fetch_recipe(food_name):
    url = "https://recipesapi2.p.rapidapi.com/recipes/"+food_name
    print(url)
    querystring = {"maxRecipes":"1"}

    headers = {
        'x-rapidapi-host': "recipesapi2.p.rapidapi.com",
        'x-rapidapi-key': "f6f6823b91msh9e92fed91d5356ap136f5djsn494d8f582fb3"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_data = json.loads(response.text)

    recipe_data = json_data['data'][0]

    return recipe_data