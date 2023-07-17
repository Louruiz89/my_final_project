#!/usr/bin/env python
# coding: utf-8

#API de ChatGPT
from dotenv import load_dotenv
import os #provides ways to access the Operating System and allows us to read the environment variables
import openai

import requests # API weather

import pandas as pd

from haversine import haversine, Unit #Import lat and long
from math import radians, sin, cos, sqrt, atan2

import streamlit as st #Create the APP


st.title("CampToGo")
st.header("Welcome user")
st.subheader("This is the APP that helps you to plan your last minute road trip in Campervan starting from Madrid")


#Llamo a la API de chatGPT aunque ahora he decidido no empezar usandola

load_dotenv()
my_secret_key = os.getenv("my_openai_key")

#Llamo a la contraseña que tengo guardada en .env

openai.api_key = my_secret_key

#Le doy la bienvenida al usuario

print("Welcome to the APP that helps you to plan your last minute road trip in Campervan starting from Madrid")

#Le pregunto al usuario cuantos días va a viajar ya que es la base de mi elección de itinerario

days = int(input("Please enter how many days are you going to travel: "))

#Creo un diccionario en base al radio de KM para usarlo como referencia para saber el tiempo

dictionary = {
    'N': ['Riaza', 'Aranda de Duero', 'Burgos', 'Santander', 'Santander'],
    'NO': ['Segovia', 'Zamora', 'Ponferrada', 'Lugo', 'A Coruña'],
    'O': ['Ávila', 'Salamanca', 'Ciudad Rodrigo', 'Ciudad Rodrigo', 'Ciudad Rodrigo'],
    'SO': ['Talavera de la Reina', 'Plasencia', 'Mérida', 'Sevilla', 'Huelva'],
    'S': ['Toledo', 'Ciudad Real', 'Jaén', 'Granada', 'Málaga'],
    'SE': ['Saelices', 'Albacete', 'Almansa', 'Murcia', 'Almería'],
    'E': ['Sacedón', 'Cuenca', 'Valencia', 'Jávea', 'Alicante'],
    'NE': ['Sigüenza', 'Calatayud', 'Zaragoza', 'Huesca', 'Andorra']}


#Necesito restar los días -2 para que me de la posición correcta del diccionario ya que por ejemplo 
# en 3 días de viaje quiero hacer como máximo 200 kms, es decir la 2 posición que en python es 1
''''''
if days >=8:
    d = 5
elif days == 7 or days >= 2: 
    d = int(days - 2)
else:
    d = 0
    
d


#Creo una función para que me genere automaticamente las ubicaciones en base a los días de viaje

def get_places(dictionary, d):
    values = {}
    for key, value_list in dictionary.items():
        if d < len(value_list):
            values[key] = value_list[d]
    return values


# In[11]:


#Reviso que me devuelva el resultado correcto https://www.weatherapi.com/docs/

result = get_places(dictionary, d)
print(result)


# In[12]:


#Creo todas las variables para llamar a la API del tiempo menos "q" que representa el lugar 
#de dónde quiero ver la previsión del tiempo
load_dotenv()
url = 'http://api.weatherapi.com/v1'
forecast = '/forecast.json?'
pre = 'key='
key =os.getenv("my_weather_token")
wdays = '&days=1'
final = '&aqi=no&alerts=no'

#print(url + forecast + pre + key + wdays + final)


# In[13]:


#Ahora creo una variable "q" para cada punto cardinal

q_var = '&q='
norte = q_var + result['N']
noroeste = q_var + result['NO']
oeste = q_var + result['O']
suroeste = q_var + result['SO']
sur = q_var + result['S']
sureste = q_var + result['SE']
este = q_var + result['E']
noreste = q_var + result['NE']


# In[14]:


#Creo una llamada a la API para cada lugar

check_rain_north = requests.get(url + forecast + pre + key + norte + wdays + final)
check_rain_nortwest = requests.get(url + forecast + pre + key + noroeste + wdays + final)
check_rain_west = requests.get(url + forecast + pre + key + oeste + wdays + final)
check_rain_southwest = requests.get(url + forecast + pre + key + suroeste + wdays + final)
check_rain_south = requests.get(url + forecast + pre + key + sur + wdays + final)
check_rain_southeast = requests.get(url + forecast + pre + key + sureste + wdays + final)
check_rain_east = requests.get(url + forecast + pre + key + este + wdays + final)
check_rain_northeast = requests.get(url + forecast + pre + key + noreste + wdays + final)

#check_rain_southeast.status_code


# In[15]:


check_rain_north_result = check_rain_north.json()
check_rain_nortwest_result = check_rain_nortwest.json()
check_rain_west_result = check_rain_west.json()
check_rain_southwest_result = check_rain_southwest.json() 
check_rain_south_result = check_rain_south.json() 
check_rain_southeast_result = check_rain_southeast.json()
check_rain_east_result = check_rain_east.json()
check_rain_northeast_result = check_rain_northeast.json()


# In[16]:


print("Awesome! I suggest to travel to the following directions as the others could rain tomorrow")

#North
if check_rain_north_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0:
    print('North')
    
#Northwest
if check_rain_nortwest_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0:
    print('Northwest')

#West
if check_rain_west_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0:
    print('West')
    
#Southwest
if check_rain_southwest_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0:
    print('Southwest')
    
#South
if check_rain_south_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0:
    print('South')

#Southeast
if check_rain_southeast_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0:
    print('Southeast')

#East
if check_rain_east_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0:
    print('East')
    
#Northeast
if check_rain_northeast_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0:
    print('Northeast')


# In[17]:


#Ahora le pido al usuario que elija el punto cardinal

direction = input('Choose one: ')


# In[18]:


#Cargo el dataset de municipios para tener las coordenadas

municipios = pd.read_csv('./data/pueblos_bonitos_punto.csv')
municipios[:8]


# In[19]:


#Cargo el dataset de las coordenadas de mis puntos cardinales para calcular las distancias

p_cardinales = pd.read_csv('./data/puntos_cardinales_punto.csv')
p_cardinales


# In[20]:


#Ahora hago match entre la dirección que ha elegido el usuario y las opciones que tengo

def user_direction(direction, result):
    if direction == 'north' or direction == 'N' or direction == 'North':
        return result['N']
    elif direction == 'northwest' or direction == 'NW' or direction == 'Northwest' or direction == 'NorthWest':
        return result['NO']
    elif direction == 'west' or direction == 'West' or direction == 'W':
        return result['O']
    elif direction == 'southwest' or direction == 'Southwest' or direction == 'SouthWest' or direction == 'SW':
        return result['SO']
    elif direction == 'south' or direction == direction == 'S' or direction == 'South':
        return result['S']
    elif direction == 'southeast' or direction == 'Southeast' or direction == 'SouthEast' or direction == 'SE':
        return result['SE']
    elif direction == 'east' or direction == 'East' or direction == 'E':
        return result['E']
    elif direction == 'northeast' or direction == 'Northeast' or direction == 'NorthEast' or direction == 'NE':
        return result['NE']
    else:
        return 'I am not able to find the direction'


# In[21]:


#Guardo el resultado en un diccionario

result = {'N': result['N'], 'NO': result['NO'], 'O': result['O'], 'NE': result['NE'],
          'S': result['S'], 'SO': result['SO'], 'SE': result['SE'], 'E': result['E']}




output = user_direction(direction, result)
output




#Guardo en las variables de latitud y longitud desde dónde quiero crear el radio de los pueblos que recomendar

row = p_cardinales[p_cardinales['Pueblo'] == output]
row


# In[25]:


idx = row.index[row['Pueblo'] == output][0]
idx




lat_origen = row['Latitud'][idx]
long_origen = row['Longitud'][idx]




def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Calculate differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate distance
    distance = R * c
    return distance


# In[33]:


municipios["Distance"] = municipios.apply(lambda row: haversine(row["Latitud"], row["Longitud"], lat_origen, long_origen), axis=1)
municipios


# In[34]:


top_3 = municipios.sort_values(by='Distance').reset_index(drop=True)[:3]
top_3


# In[35]:


one = top_3.iloc[0, top_3.columns.get_loc('Pueblo')]
two = top_3.iloc[1, top_3.columns.get_loc('Pueblo')]
three = top_3.iloc[2, top_3.columns.get_loc('Pueblo')]


# In[36]:


print('Cool! I recommend you to visit these 3 villages selected as Pueblos Bonitos de España: ') 
print(one)
print(two)
print(three)


# In[37]:


print('Now, let me give you some tips. Find below what to visit, where you can park to sleep and popular routes for trekking')


# In[38]:


def generate_monuments_prompt(place):
    chat_prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"List the top places to visit in {place} but\
        don't explain them and do not give me a introduction , just the answer with\
        the list. After that, let me know where I should park to sleep in a campervan.\
        Last, list me the 3 most common tracking routes and show me the amount of kilometers\
        and the difficulty level rated by easy, medium or high."}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_prompt
    )

    return response.choices[0].message.content.strip()


# In[39]:


place = one 


# In[40]:


response_text = generate_monuments_prompt(place)
print(one)
print(response_text)


# In[41]:


place = two


# In[42]:


response_text = generate_monuments_prompt(place)
print(two)
print(response_text)


# In[43]:


place = three


# In[44]:


response_text = generate_monuments_prompt(place)
print(three)
print(response_text)


# In[45]:


print('Enjoy your trip!') 


# In[ ]:




