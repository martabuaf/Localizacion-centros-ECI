##Librerías

import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup

from time import sleep

from selenium import webdriver # Chrome
import helium

import folium
from folium import plugins

##Paso 1: Obtengo las url de todos los centros

url_inicio = "https://www.elcorteingles.es/centroscomerciales/es/eci/centros?page=1"

url_fin = "https://www.elcorteingles.es/centroscomerciales/es/eci/centros?page=5"

url_list = list()

for i in range(1, 6):
    
    url = f"https://www.elcorteingles.es/centroscomerciales/es/eci/centros?page={i}"
    
    session = requests.Session()

    session.headers["User-Agent"] ="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"

    response = session.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    
    links = [s["href"] for s in soup.find_all("a", class_ = "service")] #Se muestran sólo las extensiones
     
    url_list.extend(links)
    
    sleep(1)

##Paso 2: Obtengo la informacion de todos los centros

centros = list()
imagenes = list()
ciudades = list()
direcciones = list()
telefonos = list()
coordenadas = list()
webs = list()

for url_extension in url_list:

    url_body = "https://www.elcorteingles.es"

    url = f"https://www.elcorteingles.es{url_extension}"
    
    session = requests.Session()

    session.headers["User-Agent"] ="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"

    response = session.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        centro = soup.find("h1", class_ = "text-center").text.replace("Centro Comercial de ", "")
    except:
        centro = np.nan

    try:
        imagen_extension = soup.find("img", alt="Imagen principal de la tienda")["src"]
        imagen = f"https://www.elcorteingles.es{imagen_extension}"
    except:
        imagen = np.nan

    try:
        ciudad = soup.find("p", class_ = "text-center subtitle").text
    except:
        ciudad = np.nan

    try:
        direccion = soup.find("div", class_ = "building").find("dd").text
    except:
        direccion = np.nan

    try:
        telefono = soup.find("a", class_ = "phone").text.strip()
    except:
        telefono = np.nan

    try:
        lat = soup.find("div", class_ = "localization").find("script").text.split("lat:")[1].split(",")[0]
        lng = soup.find("div", class_ = "localization").find("script").text.split("lng:")[1].split("}")[0]
        coordenada = [lat, lng]
    except:
        coordenada = np.nan
        
    centros.append(centro)
    imagenes.append(imagen)
    ciudades.append(ciudad)
    direcciones.append(direccion)
    telefonos.append(telefono)
    coordenadas.append(coordenada)
    webs.append(url)
    
    sleep(1)

df_ECI = pd.DataFrame()

df_ECI["Centro"] = centros
df_ECI["Ciudad"] = ciudades
df_ECI["Dirección"] = direcciones
df_ECI["Teléfono"] = telefonos
df_ECI["Coordenadas"] = coordenadas
df_ECI["Imagen"] = imagenes
df_ECI["Sitio Web"] = webs
    
df_ECI.to_csv()

##Paso 3: Representar los centros en el mapa (Mapa autoescalable)

#mapa_ECI = folium.Map(location = [40.4637, -3.7492], zoom_start = 6, tiles = "CartoDB Positron")

mapa_ECI = folium.Map(tiles = "CartoDB Positron")

coordenadas = df_ECI["Coordenadas"].values

#Convierto los datos de la lista a float

for enumi, i in enumerate(coordenadas):
    for enumj, j in enumerate(i):
        coordenadas[enumi][enumj] = float(j)
        
# Creamos el mapa

for i in range(len(df_ECI)):

    coord = coordenadas[i]
    centro = df_ECI.iloc[i]["Centro"]
    ciudad = df_ECI.iloc[i]["Ciudad"]
    direccion = df_ECI.iloc[i]["Dirección"]
    telefono = df_ECI.iloc[i]["Teléfono"]
    imagen = df_ECI.iloc[i]["Imagen"]
    web = df_ECI.iloc[i]["Sitio Web"] 

    html=f"""
        <div style="text-align: center;">
            <img class="center-image" src="{imagen}" alt="Imagen principal del centro" style="width:150px;height:auto;">
        </div>
        <h3 style="font-family:Verdana;font-size:14px;"">{centro}</h3>
        <h4 style="font-family:Verdana;font-size:12px;">{ciudad}</h4>       
        <p style="font-family:Verdana;font-size:10px;"><b>Direccion </b>{direccion}</p>
        <p style="font-family:Verdana;font-size:10px;"><b>Teléfono </b>{telefono}</p>
        <p style="font-family:Verdana;font-size:10px;">Ir al <a href="{web}" target = "_blank">sitio web </a></p>
         """

    icon = folium.features.CustomIcon("https://www.elcorteingles.es/recursos/informacioncorporativa/img/portal/2017/07/06/el-corte-ingles-triangulo.png", icon_size=(50,25))

    iframe = folium.IFrame(html = html, width = 200, height = 200)

    popup = folium.Popup(iframe, max_width=200)

    folium.Marker(location = coord, icon=icon, popup = popup).add_to(mapa_ECI)

mapa_ECI.fit_bounds(mapa_ECI.get_bounds()) #Encuadra el mapa automáticamente

mapa_ECI.save("mapa_ECI.html")

##Paso 4: Añadir sistema de ubicación de centros por código postal

#Pedir al usuario un codigo postal

latlng = pd.read_excel("listado-codigos-postales-con-LatyLon.xlsx")

latlng["codigopostalid"] = latlng["codigopostalid"].astype("str")

prompt = True

print("Introduce un código postal y te mostraremos los centros El Corte Inglés más cercanos.")

while prompt == True:
    
    cp = input("Código Postal: ")
    
    if cp in latlng["codigopostalid"].to_list():
        
        prompt = False
        
    else:
        
        print("El código postal que has introducido es incorrecto, por favor vuelve a intentarlo.")

indice = latlng.index[latlng["codigopostalid"] == cp]

lat = latlng.iloc[indice]["lat"].values[0]

lng = latlng.iloc[indice]["lon"].values[0]

mapa_ECI = folium.Map(location = [lat, lng], zoom_start = 13, tiles = "CartoDB Positron")

coordenadas = df_ECI["Coordenadas"].values

#Convierto los datos de la lista a float

for enumi, i in enumerate(coordenadas):
    for enumj, j in enumerate(i):
        coordenadas[enumi][enumj] = float(j)
        
#Distancia en km desde la ubicación del CP hasta el centro más cercano

import geopy.distance

distancia_list = list()

for i in range(len(df_ECI)):

    origen = [lat, lng]
    
    destino = df_ECI.iloc[i]["Coordenadas"]

    distancia = round(geopy.distance.geodesic(origen, destino).km, 2)
    
    distancia_list.append(distancia)

distancia_min = min(distancia_list)    
    
print(f"El centro El Corte Inglés más cercano se encuentra a {distancia_min} km.")
        
# Creamos el mapa

for i in range(len(df_ECI)):

    coord = coordenadas[i]
    centro = df_ECI.iloc[i]["Centro"]
    ciudad = df_ECI.iloc[i]["Ciudad"]
    direccion = df_ECI.iloc[i]["Dirección"]
    telefono = df_ECI.iloc[i]["Teléfono"]
    imagen = df_ECI.iloc[i]["Imagen"]
    web = df_ECI.iloc[i]["Sitio Web"] 

    html=f"""
        <div style="text-align: center;">
            <img class="center-image" src="{imagen}" alt="Imagen principal del centro" style="width:150px;height:auto;">
        </div>
        <h3 style="font-family:Verdana;font-size:14px;"">{centro}</h3>
        <h4 style="font-family:Verdana;font-size:12px;">{ciudad}</h4>       
        <p style="font-family:Verdana;font-size:10px;"><b>Direccion </b>{direccion}</p>
        <p style="font-family:Verdana;font-size:10px;"><b>Teléfono </b>{telefono}</p>
        <p style="font-family:Verdana;font-size:10px;">Ir al <a href="{web}" target = "_blank">sitio web </a></p>
         """

    icon = folium.features.CustomIcon("https://www.elcorteingles.es/recursos/informacioncorporativa/img/portal/2017/07/06/el-corte-ingles-triangulo.png", icon_size=(50,25))

    iframe = folium.IFrame(html = html, width = 200, height = 200)

    popup = folium.Popup(iframe, max_width=200)

    folium.Marker(location = coord, icon=icon, popup = popup).add_to(mapa_ECI)

mapa_ECI.save("mapa_ECI_CP.html")

#Más iconos de la cadena ECI en: https://www.elcorteingles.es/informacioncorporativa/es/comunicacion/identidad-corporativa/
