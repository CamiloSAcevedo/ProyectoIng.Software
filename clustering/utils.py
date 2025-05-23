import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
import joblib
import os
from datetime import datetime
from django.conf import settings
import numpy as np
import unicodedata
import re
from administrador.models import Vacante  

import os
import google.generativeai as genai
from dotenv import load_dotenv
import json


# === Obtener las columnas de las vacantes ===
def obtener_columnas_disponibles():
    return [field.name for field in Vacante._meta.fields if field.name != 'id' and field.name != 'grupo' and field.name != 'modelo_clustering']


# === Transformador personalizado para aplicar pesos ===

class PesoTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, pesos):
        self.pesos = pesos  # dict: {"col1": 1.0, "col2": 0.5, ...}

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_ = X.copy()
        for i, col in enumerate(X.columns):
            peso = self.pesos.get(col, 1.0)
            X_[col] = X_[col].astype(str).apply(lambda x: (x + ' ') * int(peso))
        return X_


# === Funciones de normalización ===

def limpiar_texto(texto):
    texto = unicodedata.normalize('NFKD', str(texto)).encode('ASCII', 'ignore').decode('utf-8')
    texto = texto.lower().strip()
    texto = re.sub(r'\s+', ' ', texto)
    return texto

def normalizar_vacante(vacante):
    texto = limpiar_texto(vacante)
    if "asesor" in texto:
        return "asesor"
    if "auxiliar" in texto:
        return "auxiliar"
    if "analista" in texto:
        return "analista"
    if "tecnico" in texto:
        return "tecnico"
    return texto

def normalizar_empresa(empresa):
    texto = limpiar_texto(empresa)
    if "grupo exito" in texto or "exito" in texto:
        return "grupo exito"
    return texto

def normalizar_ubicacion(ubicacion):
    texto = limpiar_texto(ubicacion)
    if "medellin" in texto:
        return "medellin"
    if "itagui" or "itagüi" in texto:
        return "itagui"
    if "bello" in texto:
        return "bello"
    if "sabaneta" in texto:
        return "sabaneta"
    if "bogota" in texto:
        return "bogota"
    if "cali" in texto:
        return "cali"
    return texto

def normalizar_descripcion(desc):
    texto = limpiar_texto(desc)
    keywords = ["ventas", "servicio", "logistica", "produccion", "soporte", "contabilidad"]
    for palabra in keywords:
        if palabra in texto:
            return palabra
    return texto

def normalizar_industria(industria):
    texto = limpiar_texto(industria)
    if "retail" in texto or "comercial" in texto:
        return "retail"
    if "tecnologia" in texto or "software" in texto:
        return "tecnologia"
    if "salud" in texto or "medico" in texto:
        return "salud"
    return texto

def normalizar_experiencia(exp):
    texto = limpiar_texto(str(exp))
    if "sin" in texto or "no requiere" in texto:
        return "sin experiencia"
    if "1 ano" in texto or "un ano" in texto or "1 año" in texto:
        return "1 año"
    if "2" in texto:
        return "2 años"
    if "3" in texto:
        return "3 años"
    if "4" in texto or "5" in texto:
        return "4-5 años"
    return texto


# === Asignación de cluster ===

def asignar_cluster(datos_dict, modelo_clustering):
    """
    datos_dict: dict con campos como 'ubicacion', 'industria', etc.
    modelo_clustering: instancia de tu modelo guardado (tiene ruta a archivo .pkl).
    """
    import pandas as pd
    import joblib

    # Cargar el modelo
    encoder, pesos, kmeans = joblib.load(modelo_clustering.archivo_modelo)

    # Convertir a DataFrame
    df = pd.DataFrame([datos_dict])
    df.fillna('', inplace=True)

    # Normalización (misma lógica que en el entrenamiento)
    normalizadores = {
        "vacante": normalizar_vacante,
        "empresa": normalizar_empresa,
        "ubicacion": normalizar_ubicacion,
        "descripcion": normalizar_descripcion,
        "industria": normalizar_industria,
        "experiencia": normalizar_experiencia,
    }

    columnas_usadas = modelo_clustering.columnas_usadas

    for col in columnas_usadas:
        if col in normalizadores and col in df.columns:
            df[col] = df[col].apply(normalizadores[col])

    # Codificar con el mismo encoder entrenado
    encoded = encoder.transform(df[columnas_usadas])

    # Aplicar pesos
    weighted = encoded.copy()
    start = 0
    for col in columnas_usadas:
        n = len(encoder.categories_[columnas_usadas.index(col)])
        peso = pesos.get(col, 1.0)
        weighted[:, start:start+n] *= peso
        start += n

    # Predecir el cluster
    grupo = kmeans.predict(weighted)[0]
    return grupo


# === Entrenamiento del modelo ===

def entrenar_modelo_personalizado(df, columnas, pesos):
    df = df.fillna('')

    # Normalización automática por columna
    normalizadores = {
        "vacante": normalizar_vacante,
        "empresa": normalizar_empresa,
        "ubicacion": normalizar_ubicacion,
        "descripcion": normalizar_descripcion,
        "industria": normalizar_industria,
        "experiencia": normalizar_experiencia,
    }

    for col in columnas:
        if col in normalizadores:
            df[col] = df[col].apply(normalizadores[col])

    # Codificación One-Hot
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    encoded = encoder.fit_transform(df[columnas])

    # Aplicación de pesos
    weighted = encoded.copy()
    start = 0
    for col in columnas:
        n = len(encoder.categories_[columnas.index(col)])
        peso = pesos.get(col, 1.0)
        weighted[:, start:start+n] *= peso
        start += n

    # Entrenar KMeans
    kmeans = KMeans(n_clusters=5, random_state=42)
    kmeans.fit(weighted)

    # Guardar modelo
    version = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"clustering_model_{version}.pkl"
    path = os.path.join(settings.MEDIA_ROOT, 'modelos_clustering', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump((encoder, pesos, kmeans), path)

    return path, version


# === DEFINIR TARGETING CON IA ===#


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

import re
import json

def extraer_json(texto):
    match = re.search(r"```json\s*(\{.*?\})\s*```", texto, re.DOTALL)
    if match:
        return match.group(1)
    # Si no hay bloque markdown, intenta encontrar el JSON directamente
    match = re.search(r"(\{.*\})", texto, re.DOTALL)
    if match:
        return match.group(1)
    raise ValueError("No se encontró JSON en la respuesta")


def generar_targeting_desde_gemini(descripcion):
    prompt = f"""
    Analiza estas vacantes y genera un targeting válido para Meta con los siguientes campos:
    - meta_location (ejemplo: "Bogotá")
    - interests (lista en inglés, compatibles con Meta)
    - education_level (ejemplo: "college", "high_school")
    - age_min (entero)
    - age_max (entero)

    Aquí tienes las pociones disponibles para algunos de los campos:
    META_INTEREST_CHOICES = [
        ("technology", "Technology"),
        ("software_development", "Software Development"),
        ("data_science", "Data Science & Analytics"),
        ("digital_marketing", "Digital Marketing"),
        ("finance", "Finance & Accounting"),
        ("healthcare", "Healthcare"),
        ("human_resources", "Human Resources"),
        ("education_training", "Education & Training"),
        ("customer_service", "Customer Service"),
        ("sales", "Sales"),
        ("logistics", "Logistics & Supply Chain"),
    ]

    META_EDUCATION_CHOICES = [
        ("high_school", "High School"),
        ("college", "College"),
        ("associate_degree", "Associate Degree"),
        ("in_graduate_school", "In Graduate School"),
        ("doctorate_degree", "Doctorate Degree"),
    ]

    META_LOCATION_CHOICES = [
        ("New York", "New York"),
        ("Bogotá", "Bogotá"),
        ("Mexico City", "Mexico City"),
        ("Lima", "Lima"),
        ("Madrid", "Madrid"),
    ]

    Devuelve **únicamente el JSON puro sin ningún texto extra, ni etiquetas Markdown ni explicaciones**.
    Recuerda generar un solo targeting que combine las características comunes de las vacantes.

    Lista de vacantes:
    {descripcion}
    """

    response = model.generate_content(prompt)
    texto = response.text.strip()
    

    json_str = extraer_json(texto)
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error al parsear JSON:\n{json_str}\nDetalle: {e}")

