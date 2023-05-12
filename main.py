from fastapi import FastAPI
from typing import Union, Optional
from pydantic import BaseModel
import pandas as pd
import numpy as np


app = FastAPI()

class Movie(BaseModel):
    title: str
    year: int
    rating: float
    genre: str
    collection: Optional[str]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/movies")
def insertar_movies(Movie: Movie):
    return {"message": f"La pelicula {Movie.title} del anio {Movie.year} ha sido insertada"}



# --------------------------------------------------------



@app.get('/peliculas_mes/{mes}')
def peliculas_mes(mes: str) -> dict:
    # Diccionario para hacer la traducción de nombres de mes de español a inglés
    meses_dict = {"enero":"January", "febrero":"February", "marzo":"March", "abril":"April", "mayo":"May", "junio":"June",
                  "julio":"July", "agosto":"August", "septiembre":"September", "octubre":"October", "noviembre":"November",
                  "diciembre":"December"}
    
    # Cargamos el archivo CSV
    df = pd.read_csv("movies_ds_nuevo.csv")

    # Convierte la columna "release_date" a formato de fecha
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

    # Traduce el nombre de mes ingresado a su equivalente en inglés
    mes_en = meses_dict.get(mes.lower(), None)
    if mes_en is None:
        return {"error": "El mes ingresado no es válido"}

    # Filtra las películas que se estrenaron en el mes especificado
    peliculas_filtradas = df[df["release_date"].dt.month == pd.to_datetime(mes_en, format="%B").month]

    # Cuenta la cantidad de películas filtradas
    cantidad_peliculas = len(peliculas_filtradas)

    # Traduce el nombre del mes en inglés de vuelta a español
    mes_es = [key for key, value in meses_dict.items() if value == mes_en][0]

    return {"mes": mes_es.capitalize(), "cantidad": cantidad_peliculas}


@app.get('/peliculas_dia/{dia}')
def peliculas_dia(dia: str) -> dict:
    # Leer el dataset de películas
    peliculas = pd.read_csv('movies_ds_nuevo.csv')

    dia_num = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'].index(dia)

    # convertimos la columna 'release_date' a datetime (just in case)
    peliculas['release_date'] = pd.to_datetime(peliculas['release_date'], format='%Y-%m-%d')

    # Filtrar películas que se estrenaron en el día de la semana dado
    peliculas_en_dia = peliculas[peliculas['release_date'].dt.weekday == dia_num]

    # Filtrar películas que tengan una fecha de estreno válida
    peliculas_con_fecha_valida = peliculas_en_dia[peliculas_en_dia['release_date'].notnull()]

    cantidad = peliculas_con_fecha_valida.shape[0]

    # Retornar un diccionario con el día y la cantidad de películas
    return {'dia': dia, 'cantidad': cantidad}


@app.get('/franquicia/{franquicia}')
def franquicia(franquicia: str) -> dict:
    
    # Cargamos el archivo csv con los datos de las películas
    df = pd.read_csv("movies_ds_nuevo.csv")

    # Filtramos las películas que pertenecen a la franquicia solicitada
    peliculas_filtradas = df[df["belongs_to_collection"] == franquicia]

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