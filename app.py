import streamlit as st
import numpy as np
import time

import tensorflow as tf
from utils import load_prepare_image, model_pred, fetch_recipe

IMG_SIZE = (224, 224)
model_V1 = 'models\Seefood_model_v1.tflite'
model_V2 = 'models\Seefood_model_V2.tflite'

@st.cache()
def model_prediction(model, img_file, rescale):
    img = load_prepare_image(img_file, IMG_SIZE, rescale=rescale)
    prediction = model_pred(model, img)
    recipe_data = fetch_recipe(prediction)
    return prediction, recipe_data


def main():
    st.set_page_config(
        page_title="SeeFood",
        page_icon="🍔",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title('SeeFood🍔')
    st.write('Get Recipe of your food')

    col1, col2 = st.columns(2)

    with col1: 
        # image uploading button
        uploaded_file = st.file_uploader("Choose a file")
        selected_model = st.selectbox('Select Model',('model 1', 'model 2'), index=1)
        if uploaded_file is not None:
            uploaded_img = uploaded_file.read()

            col2.image(uploaded_file, width=500)

        # butoon to make predictions
        predict = st.button('Get Recipe!')

    if predict:
        if uploaded_file is not None:
            with st.spinner('Please Wait 👩‍🍳'):

                # setting model and rescalling 
                if selected_model == 'model 2':
                    pred_model = model_V2 
                    pred_rescale = True
                else:
                    pred_model = model_V1 
                    pred_rescale = False
                
                # makeing prediction and fetching food recipe form api
                food, recipe_data = model_prediction(pred_model, uploaded_img, pred_rescale)
                
                # food name message
                col1.success(f"It's an {food}")
                
                # desplay food recipe
                st.header(recipe_data['name']+" Recipe")
                
                col3, col4 = st.columns(2)
                # with st.spinner(f'Getting Recipe for {food}'):
                #     time.sleep(5)
                with col3:
                    # Ingridents of recipie
                    st.subheader('Ingredients')
                    for i in recipe_data['ingredients']:
                        st.markdown(f"* {i}")
                # Inctuction for recipe
                with col4:
                    st.subheader('Instructions')
                    for i in recipe_data['instructions']:
                        st.markdown(f"* {i}")
                

        else:
            st.warning('Please Upload Image')

                


if __name__=='__main__': 
    main()