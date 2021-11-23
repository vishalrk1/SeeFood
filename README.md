# SeeFood
an web App to classify food dishes and then to disply recipe of that food

<p float="left">
  <img src="images/Webapp_V2.png" width="50%" />
  <img src="images/RecipeDetails.png" width="50%"/> 
</p>

# Datasets Used

- **[FOOD 101](https://www.kaggle.com/dansbecker/food-101)** for general food Model
- for **Indian Food Data** created my own dataset

# Modeling Experiments

## General Food Model
- In Model V1 pretrained EfficientNetB0 Model with last 10 layers unfreezed is used. got 68% accuracy [Notebook](https://github.com/vishalrk1/SeeFood/blob/main/Notebooks/SeeFood_General_V1.ipynb)
- In Model V2 pretrained Xception Model with last 22 layers unfreezed is used. got 76% accuracy [Notebook](https://github.com/vishalrk1/SeeFood/blob/main/Notebooks/SeeFood_General_V2.ipynb)

## Api 
- **[Nutrition API](https://rapidapi.com/spoonacular/api/recipe-food-nutrition)** is used to get all the information of food


# TODO

- prepare baseline models for general food data
- collect data for indian food model and food not food model
- creat baseline model for indian food Data, and food not food data
- buid web app with streamlit and deploy it on heroku
- deply models in flutter app
- improve models

## Contact Me


<p align="start">
    <a href="https://github.com/vishalrk1" target="_blank">
        <img alt="Github" src="https://img.shields.io/badge/Github-%23F37626.svg?style=for-the-badge&logo=github&logoColor=white" />&nbsp;
    </a>
    <a href="https://www.linkedin.com/in/vishal-karangale-126492216/" target="_blank">
        <img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-%23F37626.svg?style=for-the-badge&logo=linkedin&logoColor=white" />&nbsp;
    </a>
     <a href="https://www.instagram.com/vishal_rk1/" target="_blank">
       <img alt="Instagram" src="https://img.shields.io/badge/Instagram-%23F37626.svg?style=for-the-badge&logo=instagram&logoColor=white" />&nbsp;
    </a>
</p>