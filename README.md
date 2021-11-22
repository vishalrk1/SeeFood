# SeeFood
an web App to classify food dishes and then to disply recipe of that food

<p float="left">
  <img src="images/Webapp_V2.png" width="80" height="80"/>
  <img src="images/RecipeDetails.png" width="80" height="80"/> 
</p>

# Datasets Used

- **[FOOD 101](https://www.kaggle.com/dansbecker/food-101)** for general food Model
- for **Indian Food Data** created my own dataset

# Modeling Experiments

## General Food Model
- In Model V1 pretrained EfficientNetB0 Model with last 10 layers unfreezed is used. got 68% accuracy [Notebook](https://github.com/vishalrk1/SeeFood/blob/main/Notebooks/SeeFood_General_V1.ipynb)
- In Model V2 pretrained Xception Model with last 22 layers unfreezed is used. got 76% accuracy [Notebook](https://github.com/vishalrk1/SeeFood/blob/main/Notebooks/SeeFood_General_V2.ipynb)



# TODO

- prepare baseline models for general food data, indian food Data, and food not food data
- buid web app with streamlit and deploy it on heroku
- deply models in flutter app
- improve models