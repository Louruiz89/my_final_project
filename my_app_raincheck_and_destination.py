#!/usr/bin/env python
# coding: utf-8

#Los 3 primeros imports son para llamar a la API de ChatGPT
from dotenv import load_dotenv
import os #provides ways to access the Operating System and allows us to read the environment variables
import openai

import requests #Este import es para llamar a la API del tiempo

import pandas as pd #Este import es para cargar el CSV de latitud y longitud de todos los pueblos de españa

from haversine import haversine, Unit #Estos import son para calcular las distancias de lat y long
from math import radians, sin, cos, sqrt, atan2

import streamlit as st #Es para poder crear la APP
from PIL import Image #cargar el logo

#Cargo el dataset con los nombres de todos los municipios para que el usuario elija el punto de partida
origin_places = pd.read_csv('./data/municipios_list.csv', encoding='latin-1', sep=';')

#Transformo el dataframe en una lista para poder pasarle todas las opciones al usuario
select_origin = origin_places.values.tolist()

#Código Streamlit

image = Image.open('./data/camp_n_rolla.jpg') #logo
st.image(image, width=250) #logo
st.title("Camp :red[N] Rolla") #titulo
st.header("Hey Roller friend!") #frase bienvenida
st.subheader("_Are you ready for a last minute roadtrip in your campervan or RV?_") #subtitulo

#Cargo el dataset con las latitudes y longitudes de todas las posibles ubicaciones
origen = pd.read_csv('./data/municipios_punto.csv')

#Le pido al usuario que seleccione el origen
user_origen = st.selectbox(
    'Select your origing',
    origin_places)

print(user_origen)

#Busco la latitud y longitud del lugar que ha elegido
user_select = origen[origen['Pueblo'] == user_origen]

#Necesito averiguar su indice para quedarme solo con los datos de lat y long
user_idx = user_select.index[user_select['Pueblo'] == user_origen][0]
lat_origen = user_select['Latitud'][user_idx]
long_origen = user_select['Longitud'][user_idx]

#Consulto al usuario la distancia a la que quiere viajar en km
user_distance = st.number_input('How many km do you want to travel?: ', min_value=1, max_value=999, step=1)

#Creo una función por dirección para que me saque la long y lat en base a los km que ha marcado el usuario
def get_coordinates_south(latitude, longitude, distance_km):

    distance_meters = distance_km * 1000 #convierto a metros

    #Me devuelve las coordenadas de destino usando haversine 
    destination_lat = latitude - (distance_meters / 1000) / 111.32
    destination_lon = longitude

    return destination_lat, destination_lon

def get_coordinates_north(latitude, longitude, distance_km):

    distance_meters = distance_km * 1000

    destination_lat = latitude + (distance_meters / 1000) / 111.32
    destination_lon = longitude

    return destination_lat, destination_lon

def get_coordinates_east(latitude, longitude, distance_km):
    
    distance_meters = distance_km * 1000

    destination_lat = latitude
    destination_lon = longitude + (distance_meters / 1000) / (111.32 * abs(latitude))

    return destination_lat, destination_lon

def get_coordinates_west(latitude, longitude, distance_km):

    distance_meters = distance_km * 1000

    destination_lat = latitude
    destination_lon = longitude - (distance_meters / 1000) / (111.32 * abs(latitude))

    return destination_lat, destination_lon

def get_coordinates_northeast(latitude, longitude, distance_km):
    distance_meters = distance_km * 1000

    destination_lat = latitude + (distance_meters / 1000) / 111.32
    destination_lon = longitude + (distance_meters / 1000) / (111.32 * abs(latitude))

    return destination_lat, destination_lon

def get_coordinates_northwest(latitude, longitude, distance_km):
    
    distance_meters = distance_km * 1000

    destination_lat = latitude + (distance_meters / 1000) / 111.32
    destination_lon = longitude - (distance_meters / 1000) / (111.32 * abs(latitude))

    return destination_lat, destination_lon

def get_coordinates_southeast(latitude, longitude, distance_km):

    distance_meters = distance_km * 1000

    destination_lat = latitude - (distance_meters / 1000) / 111.32
    destination_lon = longitude + (distance_meters / 1000) / (111.32 * abs(latitude))

    return destination_lat, destination_lon

def get_coordinates_southwest(latitude, longitude, distance_km):

    distance_meters = distance_km * 1000

    destination_lat = latitude - (distance_meters / 1000) / 111.32
    destination_lon = longitude - (distance_meters / 1000) / (111.32 * abs(latitude))

    return destination_lat, destination_lon

if __name__ == "__main__":
    original_latitude = lat_origen
    original_longitude = long_origen
    distance_km = user_distance
    
    # Calculo las coordenadas para cada dirección
    south_lat, south_lon = get_coordinates_south(original_latitude, original_longitude, distance_km)
    north_lat, north_lon= get_coordinates_north(original_latitude, original_longitude, distance_km)
    east_lat, east_lon = get_coordinates_east(original_latitude, original_longitude, distance_km)
    west_lat, west_lon = get_coordinates_west(original_latitude, original_longitude, distance_km)
    northeast_lat, northeast_lon = get_coordinates_northeast(original_latitude, original_longitude, distance_km)
    northwest_lat, northwest_lon = get_coordinates_northwest(original_latitude, original_longitude, distance_km)
    southeast_lat, southeast_lon = get_coordinates_southeast(original_latitude, original_longitude, distance_km)
    southwest_lat, southwest_lon = get_coordinates_southwest(original_latitude, original_longitude, distance_km)

    # Creo un dataframe para guardar los resultados
    df_destino = pd.DataFrame({
        'Direction': ['South', 'North', 'East', 'West', 'Northeast', 'Northwest', 'Southeast', 'Southwest'],
        'Latitude': [south_lat, north_lat, east_lat, west_lat, northeast_lat, northwest_lat, southeast_lat, southwest_lat],
        'Longitude': [south_lon, north_lon, east_lon, west_lon, northeast_lon, northwest_lon, southeast_lon, southwest_lon]
    })

#Ahora reviso en cada latitud y longitud si va a llover
#Primero necesito guardar en una variable cada indice de cada dirección

user_direction_idx_s = df_destino.index[df_destino['Direction'] == 'South'][0]
user_direction_idx_n = df_destino.index[df_destino['Direction'] == 'North'][0]
user_direction_idx_e = df_destino.index[df_destino['Direction'] == 'East'][0]
user_direction_idx_w = df_destino.index[df_destino['Direction'] == 'West'][0]
user_direction_idx_ne = df_destino.index[df_destino['Direction'] == 'Northeast'][0]
user_direction_idx_nw = df_destino.index[df_destino['Direction'] == 'Northwest'][0]
user_direction_idx_se = df_destino.index[df_destino['Direction'] == 'Southeast'][0]
user_direction_idx_sw = df_destino.index[df_destino['Direction'] == 'Southwest'][0]

#Guardo la latitud y longitud de cada destino

lat_destino_s = df_destino['Latitude'][user_direction_idx_s]
long_destino_s = df_destino['Longitude'][user_direction_idx_s]
lat_destino_n = df_destino['Latitude'][user_direction_idx_n]
long_destino_n = df_destino['Longitude'][user_direction_idx_n]
lat_destino_e = df_destino['Latitude'][user_direction_idx_e]
long_destino_e = df_destino['Longitude'][user_direction_idx_e]
lat_destino_w = df_destino['Latitude'][user_direction_idx_w]
long_destino_w = df_destino['Longitude'][user_direction_idx_w]
lat_destino_ne = df_destino['Latitude'][user_direction_idx_ne]
long_destino_ne = df_destino['Longitude'][user_direction_idx_ne]
lat_destino_nw = df_destino['Latitude'][user_direction_idx_nw]
long_destino_nw = df_destino['Longitude'][user_direction_idx_nw]
lat_destino_se = df_destino['Latitude'][user_direction_idx_se]
long_destino_se = df_destino['Longitude'][user_direction_idx_se]
lat_destino_sw = df_destino['Latitude'][user_direction_idx_sw]
long_destino_sw = df_destino['Longitude'][user_direction_idx_sw]

#Guardo juntas las coordenadas de cada lugar para poder meterlas en la API

ws = str(lat_destino_s) + ',' + str(long_destino_s)
wn = str(lat_destino_n) + ',' + str(long_destino_n)
we = str(lat_destino_e) + ',' + str(long_destino_e)
ww = str(lat_destino_w) + ',' + str(long_destino_w)
wne = str(lat_destino_ne) + ',' + str(long_destino_ne)
wnw = str(lat_destino_nw) + ',' + str(long_destino_nw)
wse = str(lat_destino_se) + ',' + str(long_destino_se)
wsw = str(lat_destino_sw) + ',' + str(long_destino_sw)

#Creo todas las variables para llamar a la API del tiempo

load_dotenv()
url = 'http://api.weatherapi.com/v1'
forecast = '/forecast.json?'
pre = 'key='
key =os.getenv("my_weather_token")
wdays = '&days=1'
final = '&aqi=no&alerts=no'
q_var = '&q='

#Creo una variable especifica por cada destino para poder revisar cada ubicación

ws_weather = q_var + ws
wn_weather = q_var + wn
we_weather = q_var + we
ww_weather = q_var + ww
wne_weather = q_var + wne
wnw_weather = q_var + wnw
wse_weather = q_var + ws
wsw_weather = q_var + wsw

#Creo una llamada a la API para cada lugar

check_rain_north = requests.get(url + forecast + pre + key + wn_weather + wdays + final)
check_rain_nortwest = requests.get(url + forecast + pre + key + wnw_weather + wdays + final)
check_rain_west = requests.get(url + forecast + pre + key + ww_weather + wdays + final)
check_rain_southwest = requests.get(url + forecast + pre + key + wsw_weather + wdays + final)
check_rain_south = requests.get(url + forecast + pre + key + ws_weather + wdays + final)
check_rain_southeast = requests.get(url + forecast + pre + key + wse_weather + wdays + final)
check_rain_east = requests.get(url + forecast + pre + key + we_weather + wdays + final)
check_rain_northeast = requests.get(url + forecast + pre + key + wne_weather + wdays + final)

#Reviso si llueve en cada dirección

check_rain_north_result = check_rain_north.json()
check_rain_nortwest_result = check_rain_nortwest.json()
check_rain_west_result = check_rain_west.json()
check_rain_southwest_result = check_rain_southwest.json() 
check_rain_south_result = check_rain_south.json() 
check_rain_southeast_result = check_rain_southeast.json()
check_rain_east_result = check_rain_east.json()
check_rain_northeast_result = check_rain_northeast.json()

#Creo una función para que le enseñe al usuario solo aquellos sitios dónde no va a llover

def not_raining_places():

    placestogo = []

    if check_rain_north_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0:
        placestogo.append('North')
    if check_rain_nortwest_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0:
        placestogo.append('Northwest')
    if check_rain_west_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0: 
        placestogo.append('West')  
    if check_rain_southwest_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0: 
        placestogo.append('Southwest')
    if check_rain_south_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0:
        placestogo.append('South')
    if check_rain_southeast_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0:
        placestogo.append('Southeast')
    if check_rain_east_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0:  
        placestogo.append('East')
    if check_rain_northeast_result['forecast']["forecastday"][0]['day']['daily_chance_of_rain'] == 0:
        placestogo.append('NorthEast')
    return placestogo

placestogo_list = not_raining_places()

#Le pido al usuario que seleccione un lugar dónde no hay probabilidad de lluvia

rainning_dir = ['North', 'East', 'West', 'South']

if placestogo_list == []:
    direction = st.selectbox(":umbrella_with_rain_drops: :red[It's raining everywhere but still, let me show you some places. Although, I suggest to change other amount of km]",
                    rainning_dir
)
else:
    direction = st.selectbox(
    'Awesome! Pick up one of the following directions or if not, get ready to get wet as it could rain bro! Choose one and see cool recomendations: ',
                    placestogo_list
)

#En base a la dirección que me ha dicho el usuario, guardo la ubicación

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

#Creo un diccionario con el lugar que ha elegido el usuario

result = {'N': df_destino[df_destino['Direction'] == 'North'], 
          'NO': df_destino[df_destino['Direction'] == 'Northwest'], 
          'O': df_destino[df_destino['Direction'] == 'West'], 
          'NE': df_destino[df_destino['Direction'] == 'Northeast'],
          'S': df_destino[df_destino['Direction'] == 'South'],
          'SO': df_destino[df_destino['Direction'] == 'Southwest'],
          'SE': df_destino[df_destino['Direction'] == 'Southeast'],
          'E': df_destino[df_destino['Direction'] == 'East']}

#Genero la latitud y longitud en base a las directrices del usuario

output = user_direction(direction, result)

#Creo un dataframe con el resultado generado en output
user_dir = output

#Averiguo el indice del resultado para quedarme solo con la lat y long
user_direction_idx = output.index[output['Direction'] == direction][0]

#Guardo en variables las lat y long para poder analizar que lugares recomendados son los más cercanos
lat_destino = user_dir['Latitude'][user_direction_idx]
long_destino = user_dir['Longitude'][user_direction_idx]

#Cargo el dataset de pueblos bonitos llamado municipios para obtener las coordenadas

municipios = pd.read_csv('./data/pueblos_bonitos_punto.csv')

#Cálculo la distancia desde la elección del usuario a cada pueblo

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

#Añado una nueva columna con la distancia de mi punto de origen a cada lugar recomendado que visitar
municipios["Distance"] = municipios.apply(lambda row: haversine(row["Latitud"], row["Longitud"], lat_destino, long_destino), axis=1)

#Selecciono los 3 lugares más cercanos al punto para recomendarselos al usuario
top_3 = municipios.sort_values(by='Distance').reset_index(drop=True)[:3]

#Guardo cada resultado de forma independiente
one = top_3.iloc[0, top_3.columns.get_loc('Pueblo')]
two = top_3.iloc[1, top_3.columns.get_loc('Pueblo')]
three = top_3.iloc[2, top_3.columns.get_loc('Pueblo')]


#Llamo a la API de OpenAI para que me devuelva que ver, donde dormir y varias rutas.

load_dotenv()
my_secret_key = os.getenv("my_openai_key")

#Llamo a la contraseña que tengo guardada en .env

openai.api_key = my_secret_key

#Le hago la primera consulta

def generate_monuments_prompt(place):
    chat_prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"List the top places to visit in {place} but\
        don't explain them and do not give me a introduction , just the answer with\
        the list after the sentence:'You should visit these places'."}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_prompt
    )

    return response.choices[0].message.content.strip()

def generate_park_prompt(place):
    chat_prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Let me know where I should park to sleep in a campervan in {place}.\
         Don't explain me the parking, just let me know the place after the sentence: 'You should park here'"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_prompt
    )

    return response.choices[0].message.content.strip()

def generate_trekking_prompt(place):
    chat_prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"List me the 3 most common trekking routes in {place}\
         and show me the amount of kilometers\
        and the difficulty level rated by easy, medium or high.\
         Just list the routes and don't give me introduction or any extra information.\
         Always start the list after the sentence 'These are the top 3 most common trekking routes:'"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_prompt
    )

    return response.choices[0].message.content.strip()

place = one 
response_text = generate_monuments_prompt(place)
response_park = generate_park_prompt(place)
response_trekking = generate_trekking_prompt(place)
st.subheader(':european_castle:')
st.subheader(f'{one}')
st.write(f'{response_text}')
st.write(':tent:')
st.write(f'{response_park}')
st.write(':footprints:')
st.write(f'{response_trekking}')

place = two
response_text = generate_monuments_prompt(place)
response_park = generate_park_prompt(place)
response_trekking = generate_trekking_prompt(place)
st.subheader(':sunrise_over_mountains:')
st.subheader(f'{two}')
st.write(f'{response_text}')
st.write(':tent:')
st.write(f'{response_park}')
st.write(':footprints:')
st.write(f'{response_trekking}')

place = three
response_text = generate_monuments_prompt(place)
response_park = generate_park_prompt(place)
response_trekking = generate_trekking_prompt(place)
st.subheader(':classical_building:')
st.subheader(f'{three}')
st.write(f'{response_text}')
st.write(':tent:')
st.write(f'{response_park}')
st.write(':footprints:')
st.write(f'{response_trekking}')

st.header('Go for it and enjoy your trip!')

enjoy_image = Image.open('./data/enjoy.jpg')

st.image(enjoy_image)