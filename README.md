# Data_Analytics

## Este es un proyecto de Data Science. Aplicaremos: Webscraping + Visualizaciones

# Título : Localización de centros ElCorteInglés

Resumen:
Partiendo de la página de ECI con la lista de todos los centros en España sacaremos una lista con todas 
las url de esos centros para posteriormente entrar en cada uno y sacar la información y localización geográfica de los centros. 
Incluiremos toda la información en un dataframe que luego usaremos para visualizar los centros en un mapa interactivo.

Paso 1:
Primero necesitamos extraer la lista con todas las url de los centros ElCorteInglés que hay en España (y Portugal).
La página desde la que iniciaremos la búsqueda es: https://www.elcorteingles.es/centroscomerciales/es/eci/centros

Paso 2:
Una vez tenemos las url de todos los centros entraremos en todas las páginas para sacar la información de los centros 
(Nombre, Dirección, Teléfono, localización) y guardaremos esos datos en un DataFrame.

Paso 3:
Partiendo del DataFrame anterior visualizaremos los datos con folium en un mapa interactivo que muestre la localización 
de los centros y toda la información a modo de popup.

Paso 4:
Como ampliación del proyecto se propone añadir un sistema de búsqueda de los centros más cercanos mediante el código postal. 
El usuario introduce el CP y el sistema muestra un mapa de los centros más cercamos, así como la distancia (en km) de cada uno a este punto.
