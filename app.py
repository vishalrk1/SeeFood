import streamlit as st
import numpy as np
import time

import tensorflow as tf
from utils import load_prepare_image_tf, model_pred_tf, fetch_recipe, load_prepare_image_pt, model_pred_pt
from FoodNoFood import food_not_food
from PIL import Image

import sys
sys.path.insert(1, 'Api Data')
from RecipeData import fetchRecipeData

IMG_SIZE = (224, 224)
model_V1 = 'models/Seefood_model_v1.tflite'
model_V2 = 'models/Seefood_model_V2.tflite'
ViT_model = 'models/ViT-101-1.pt'

@st.cache(show_spinner=False)
def model_prediction(model, img_file, rescale, model_tensor_type):
    if model_tensor_type == 'TF':
        img = load_prepare_image_tf(img_file, IMG_SIZE, rescale=rescale)
        prediction = model_pred_tf(model, img)
        sorceCode, recipe_data = fetchRecipeData(prediction)
    elif model_tensor_type == 'Pt':
        img = load_prepare_image_pt(img_file)
        prediction = model_pred_pt(img, model)
        print(prediction)
        sorceCode, recipe_data = fetchRecipeData(prediction)
        
    return prediction, sorceCode, recipe_data 


def main():
    st.set_page_config(
        page_title="SeeFood",
        page_icon="🍔",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title('SeeFood🍔')
    st.write('Upload a food image and get the recipe for that food and other details of that food')

    col1, col2 = st.columns(2, gap='large')

    with col1: 
        # image uploading button
        uploaded_file = st.file_uploader("Choose a file")
        selected_model = st.selectbox('Select Model',( 'ViT Model', 'model 1', 'model 2'), index=0)
        
        if uploaded_file is not None:
            uploaded_img = uploaded_file.read()
            pil_img = Image.open(uploaded_file)

            col2.image(uploaded_file, width=700)

        # butoon to make predictions
        predict = st.button('Get Recipe!')

    if predict:
        with st.spinner("Analyzing Image 🕵️‍♂️"):
            food_cat = food_not_food(pil_img)
        
        if food_cat == 'food':
            if uploaded_file is not None:
                with st.spinner('Please Wait 👩‍🍳'):

                    # setting model and rescalling 
                    if selected_model in ['model 1', 'model 2']:
                        
                        if selected_model == 'model 2':
                            pred_model = model_V2 
                            pred_rescale = True
                        elif selected_model == 'model 1':
                            pred_model = model_V1 
                            pred_rescale = False
                        
                        # makeing prediction and fetching food recipe form api
                        food, source_code, recipe_data = model_prediction(pred_model, uploaded_img, pred_rescale, 'TF')
                        
                    elif selected_model == 'ViT Model':
                        pred_model = ViT_model 
                        pred_rescale = True
                        # makeing prediction and fetching food recipe form api
                        food, source_code, recipe_data = model_prediction(pred_model, pil_img, pred_rescale, 'Pt')
                        
                    # asssigning caleoric breakdown data
                    percent_Protein = recipe_data['percentProtein']
                    percent_fat = recipe_data['percentFat']
                    percent_carbs = recipe_data['percentCarbs'] 
                        
                    # food name message
                    col1.success(f"It's an {food}")
                        
                    if source_code == 200:
                        # desplay food recipe
                        st.header(recipe_data['title']+" Recipe")
                        
                        col3, col4 = st.columns(2, gap='medium')

                        with col3:
                            # Ingridents of recipie
                            st.subheader('Ingredients')
                            # st.info(recipe_data['ingridents'])
                            for i in recipe_data['ingridents']:
                                st.info(f"{i}")
                        # Inctuction for recipe
                        with col4:
                            st.subheader('Instructions')
                            st.info(recipe_data['instructions'])
                            # st.subheader('Caloric Breakdown')
                            '''
                            ## Caloric Breakdown
                            '''
                            st.success(f'''
                                        * Protien:  {percent_Protein}%
                                        * Fat: {percent_fat}%
                                        * Carbohydrates: {percent_carbs}%
                                    ''')
                                
                            
                    else:
                        st.error('Something went wrong please try again :(')
                    
                        
        elif food_cat == 'not food':
            with col1:
                st.warning('Invalid Image Please Add Food Image 👨‍🔧')
                    

        else:
            st.warning('Please Upload Image')

                


if __name__=='__main__': 
    main()