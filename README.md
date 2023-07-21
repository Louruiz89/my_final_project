# MY FINAL PROJECT - CAMP & ROLLA

<p align="left"><img src="https://www.rtwbackpackers.com/wp-content/uploads/2017/01/great-ocean-road-day-trip-vw-camper-hike-and-seek-melbourne-australia.jpg"></p>

## **Introduction:**

The APP **"Camp & Rolla"** borns from the idea to plan a trip in the very last minute. The best thing about having a campervan or a RV is that you can decide to travel at the last moment without having to organize anything in advance."

## **What is the application about?:**

The APP works in the following way: 

- First, the APP ask you your origin.
- Second, the APP ask how many km do you want to travel

Having this information, the APP check in 8 different directions if it's going to rain or not. 

- If there is at least 1 direction with no rain, the APP suggest you to go there and let you select the places in a menu. 
- If it's rainning in all the directions, the APP give you the advice about to select other amount of km but, eventhough it's rainning, the APP give you some idead just in case there are no options to avoid the rain. 

After your selection, the APP gives the top 3 places closer to the km you told. The APP gives you the following information of all the 3 places: 

- Top places to visit.
- A suggestion to park and sleep over. 
- 3 trekking routes and the difficulty. 

## **Libraries:**

- **import load_dotenv:** Used to save the passwords of the APIs
- **import os:** Used to save the passwords of the APIs
- **import openai:** API of Artificial Intelligence
- **import requests:** The library to call the weather API
- **import pandas:** The library to work with dataframes
- **import haversine:** Used to calculate the distances from latitude and longitude
- **import radians, sin, cos, sqrt, atan2 (from math):** Used to calculate the distances from latitude and longitude
- **import streamlit:** The library to create an application to make the code more visual
- **import Image:** To show images in the APP

## **Directory Structure**
```
├── .env
├── .gitignore
├── data
│   ├── camp_n_rolla.jpg (logo)
│   ├── enjoy.jpg (closure)
│   ├── municipios.csv
│   ├── municipios_list.csv
│   ├── municipios_punto.csv
│   ├── pueblos_bonitos.csv
│   ├── pueblos_bonitos_punto.csv
│   ├── puntos_cardinales.csv
│   └── puntos_cardinales_punto.csv
├── Datasets_conversion.ipynb
├── README.md
├── my_app_raincheck_and_destination.ipynb
└── my_app_raincheck_and_destination.py
```

## **To Do:**

As next steps, I would like to include: 
- More places to visit besides the "Pueblos Bonitos"
- Include images of the places
- Connect the Google API to get recommendations of restaurants
- Improve the code