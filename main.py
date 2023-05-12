from fastapi import FastAPI
import pandas as pd
import numpy as np


app = FastAPI()

# Cargamos nuestro archivo CSV:
df_red = pd.read_csv('movies_dataset_red.csv', low_memory=False)



@app.get("/")
def root():
    return {"message": "Bienvenidos a mi API de Peliculas...(terminar, quiza meter el readme aca para testear la API)"}


@app.get('/peliculas_mes/{mes}')
def peliculas_mes(mes: str) -> dict:
    # Diccionario para hacer la traduccion de nombres de mes de español a ingles
    meses_dict = {"enero":"January", "febrero":"February", "marzo":"March", "abril":"April", "mayo":"May", "junio":"June",
                  "julio":"July", "agosto":"August", "septiembre":"September", "octubre":"October", "noviembre":"November",
                  "diciembre":"December"}
    
    # Convierte la columna "release_date" a formato de fecha
    df_red["release_date"] = pd.to_datetime(df_red["release_date"], errors="coerce")

    # Traduce el nombre de mes ingresado a su equivalente en ingles
    mes_en = meses_dict.get(mes.lower(), None)
    if mes_en is None:
        return {"Error": "El mes ingresado no es válido"}

    # Filtra las películas que se estrenaron en el mes especificado
    peliculas_filtradas = df_red[df_red["release_date"].dt.month == pd.to_datetime(mes_en, format="%B").month]

    # Cuenta la cantidad de películas filtradas
    cantidad_peliculas = len(peliculas_filtradas)

    # Traduce el nombre del mes en ingles de vuelta a español
    mes_es = [key for key, value in meses_dict.items() if value == mes_en][0]

    return {"mes": mes_es.capitalize(), 
            "cantidad": cantidad_peliculas}


@app.get('/peliculas_dia/{dia}')
def peliculas_dia(dia: str) -> dict:
  
    dia_num = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'].index(dia)

    # Convertimos la columna 'release_date' a datetime (just in case)
    df_red['release_date'] = pd.to_datetime(df_red['release_date'], format='%Y-%m-%d')

    # Filtramos películas que se estrenaron en el día de la semana dado
    peliculas_en_dia = df_red[df_red['release_date'].dt.weekday == dia_num]

    # Filtramos películas que tengan una fecha de estreno válida
    peliculas_con_fecha_valida = peliculas_en_dia[peliculas_en_dia['release_date'].notnull()]

    cantidad = peliculas_con_fecha_valida.shape[0]

    # Retornar un diccionario con el día y la cantidad de películas
    return {'dia': dia, 
            'cantidad': cantidad}


@app.get('/franquicia/{franquicia}')
def franquicia(franquicia: str) -> dict:
   
    # Filtramos las películas que pertenecen a la franquicia solicitada
    peliculas_filtradas = df_red[df_red["belongs_to_collection"] == franquicia]

    # Contamos la cantidad de películas
    cantidad_peliculas = len(peliculas_filtradas)

    # Calculamos la ganancia total
    ganancia_total = peliculas_filtradas["revenue"].sum()

    # Calculamos la ganancia promedio
    ganancia_promedio = ganancia_total / cantidad_peliculas

    return {'franquicia': franquicia,
            'cantidad': cantidad_peliculas,
            'ganancia_total': ganancia_total,
            'ganancia_promedio': ganancia_promedio}



@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais: str) -> dict:

    # Filtramos las películas que se produjeron en el país solicitado
    peliculas_filtradas = df_red[df_red["production_countries"].str.contains(pais)]

    # Contamos la cantidad de películas
    cantidad_peliculas = len(peliculas_filtradas)

    return {'pais': pais,
            'cantidad': cantidad_peliculas}


@app.get('/productoras/{productora}')
def productoras(productora: str):
    # Crear subconjunto del DataFrame original para la productora seleccionada
    subset = df_red[df_red["production_companies"].str.contains(productora, na=False)]

    # Obtener la ganancia total y la cantidad de películas producidas por la productora seleccionada
    ganancia_total = subset["revenue"].sum() - subset["budget"].sum()
    cantidad = len(subset)

    # Retornar un diccionario con los resultados
    return {"productora": productora, 
            "ganancia_total": ganancia_total, 
            "cantidad": cantidad}


@app.get('/retorno/{pelicula}')
def retorno(pelicula: str):
    # Crear subconjunto del DataFrame original para la película seleccionada
    subset = df_red[df_red["title"] == pelicula]

    # Verificar si el subconjunto tiene al menos un elemento
    if len(subset) == 0:
        return {'error': 'Película no encontrada'}

    # Obtener la inversión, ganancia y año de lanzamiento de la película seleccionada
    inversion = subset["budget"].values[0]
    ganancia = subset["revenue"].values[0] - inversion
    anio = str(subset["release_year"].values[0])

    # Obtener el retorno de la película seleccionada a partir de la columna "return"
    retorno = subset["return"].values[0]

    # Retornar un diccionario con los resultados
    return {'pelicula': pelicula, 
            'inversion': inversion, 
            'ganancia': ganancia, 
            'retorno': retorno, 
            'anio': anio}