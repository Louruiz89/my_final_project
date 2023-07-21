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

As next steps, I would like to:
- 

## **To Do:**

The Dashboard created for this project contains the following information: 

*Note - All the categories has been anonymized by ids for privacy reasons

- **Holding:** The data is filtered by specific Holding
- **Companies:** The companies grouped in the holding
- **Journey:** All the journeys generated by each company inside of this holding
- **Address:** Start and End points
- **Latitude and Longitude** of each journey
- **User:** Worker of each company
- **Kms** traveled
- **Type of vehicle:** The category selected by each user as it could be ECO (electric or hybrid) or any of the vehicles (this category may contain ECO or any other type of vehicle) 
- **Date:** From March 2022 to May 18th 2023

## **Dashboard:**
The dashboard collects the following information in each chart: 

- **Total Kgs CO2 Compensated 2023:** The total generated in the whole holding in 2023 (until May 18th 2023)
- **Kms by Category 2023:** Pie Chart of ECO vs Cabify in Kms traveled
- **CO2 / Journey:** Map with all the journeys marked where they started. All the data is by default but you are able to select per month and scroll to see all the country. 
- **Kgs CO2 Compensated by Company:** You are able to see the information of CO2 Kgs Compensated by each company month by month. 
- **Kgs CO2 2022 vs 2023:** Bar chart comparing the same month of different years. 
- **Kgs CO2 - Top 5 users:** The top 5 users that have generated more trips and, for instance, more compensation by each company

[LINK TO TABLEAU](https://tableau.cabify.com/#/site/cabify/views/CB4CO2ParentCliente/Dashboard12_1?:iid=5)

## **Insights:**

- **Total Kgs CO2 Compensated 2023:** First impact of how many KGs are generated by a holding to understand how important is to know and share the information. 
- **Kms by Category 2023:** The main category selected is Cabify. People need to increase the demanding in the ECO category. The holding should push this category as mandatory.
- **CO2 / Journey:** It's easy to know where the journeys are focused and maybe the company can present a green project where the impact is higher. 
- **Kgs CO2 Compensated by Company:** It's easy to find quick which company is generated the biggest amount of trips and compensated more CO2. 
- **Kgs CO2 2022 vs 2023:** The compensation is getting higher (surely due Covid situation as there were lower amount of trips) but it's a good chart for the incoming months. 
- **Kgs CO2 - Top 5 users:** Again, it's a great hint to know how many Kgs of CO2 a person could generate just for business trips. Each company could make a follow up on the top users to find the more sustainability  way to travel. 