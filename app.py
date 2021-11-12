import streamlit as st
import numpy as np
import time

import tensorflow as tf
from utils import load_prepare_image, model_pred, fetch_recipe

IMG_SIZE = (224, 224)
model = 'models\Seefood_model_v1.tflite'

@st.cache()
def model_prediction(img_file):
    img = load_prepare_image(img_file, IMG_SIZE)
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
        if uploaded_file is not None:
            uploaded_img = uploaded_file.read()

            col2.image(uploaded_file, width=500)

        # butoon to make predictions
        predict = st.button('Get Recipe!')

    if predict:
        if uploaded_file is not None:
            with st.spinner('Please Wait 👩‍🍳'):
                # makeing prediction and fetching food recipe form api
                food, recipe_data = model_prediction(uploaded_img)
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