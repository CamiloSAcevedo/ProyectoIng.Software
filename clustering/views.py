from django.shortcuts import render, redirect
from .forms import EntrenamientoForm
from .models import ModeloEntrenado
import pandas as pd
import joblib, os, json
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EntrenamientoForm
from .models import ModeloEntrenado
from administrador.forms import UploadFileForm
from .utils import entrenar_modelo_personalizado
from .utils import obtener_columnas_disponibles  

from administrador.models import Vacante
from collections import defaultdict

from django.shortcuts import render, get_object_or_404, redirect
from .models import ClusterTargeting
from .forms import ClusterTargetingForm

import tempfile
import json  
import os

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import generar_targeting_desde_gemini  # lo haremos abajo
'''
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")'''

def entrenar_modelo(request):
    columnas_disponibles = obtener_columnas_disponibles()
    df = None

    if request.method == "POST":
        if 'archivo_excel' in request.FILES:
            # Cargar archivo temporalmente
            excel_file = request.FILES['archivo_excel']
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                for chunk in excel_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            df = pd.read_excel(tmp_path)
            columnas_disponibles = list(df.columns)

        form = EntrenamientoForm(request.POST, request.FILES, columnas_disponibles=columnas_disponibles)

        if form.is_valid():
            columnas = form.cleaned_data['columnas']
            
            # Leer los pesos personalizados
            pesos = {
                col: form.cleaned_data.get(f"peso_{col}", 1.0)
                for col in columnas
            }

            archivo_excel = request.FILES['archivo_excel']
            df = pd.read_excel(archivo_excel)
            
            # Entrenamiento del modelo
            modelo_path, version = entrenar_modelo_personalizado(df, columnas, pesos)
            nombre = form.cleaned_data['nombre']

            # Guardar en la base de datos
            ModeloEntrenado.objects.create(
                nombre=nombre,
                archivo_modelo=modelo_path,
                columnas_usadas=columnas,
                pesos_columnas=json.dumps(pesos)  # Guardar como JSON si el campo es TextField
            )

            messages.success(request, "Modelo entrenado exitosamente.")
            return redirect('entrenar_modelo')

    else:
        form = EntrenamientoForm(columnas_disponibles=columnas_disponibles)

    return render(request, 'entrenar_modelo.html', {'form': form})



def ver_modelos_entrenados(request):
    modelos = ModeloEntrenado.objects.order_by('-fecha')
    return render(request, 'mis_modelos.html', {'modelos': modelos})


def ver_clusters(request):
    modelos = ModeloEntrenado.objects.order_by('-fecha')
    vacantes = None  # inicializamos en None
    modelo = None
    cluster = 0

    if request.method == "POST":
        cluster = request.POST.get("cluster")
        modelo_id = request.POST.get("modelo_clustering_id")
        modelo = ModeloEntrenado.objects.filter(id=modelo_id).first()

        if not cluster or not modelo_id:
            messages.error(request, "Debes seleccionar un modelo y un cluster.")
            return redirect("mis_clusters")

        vacantes = Vacante.objects.filter(modelo_clustering=modelo_id, grupo=cluster)

        return render(request, 'mis_clusters.html', {
            'modelos': modelos,
            'vacantes': vacantes,
            'modelo' : modelo,
            'cluster':cluster,
        })
    
    return render(request, 'mis_clusters.html', {
            'modelos': modelos,
            'vacantes': vacantes,
            'modelo' : modelo,
            'cluster':cluster,
        })


def definir_targeting(request, modelo_id, cluster):
    modelo = get_object_or_404(ModeloEntrenado, pk=modelo_id)
    intereses_posibles = ['Logistics', 'Sales', 'Engineering', 'Data Analysis', 'Retail Management']  

    if request.method == 'POST':
        form = ClusterTargetingForm(request.POST)
        if form.is_valid():
            targeting = form.save(commit=False)
            targeting.modelo_clustering = modelo
            targeting.cluster = cluster
            targeting.save()
            return redirect('mis_clusters')
        else:
            messages.error(request, message="Error al crear el targeting...")
    else:
        form = ClusterTargetingForm()

    return render(request, 'definir_targeting.html', {'form': form, 'cluster': cluster, 'modelo' : modelo, 'interests' : intereses_posibles})


@csrf_exempt
def generar_targeting_ia(request, modelo_id, cluster):
    if request.method == 'POST':
        try:
            modelo = ModeloEntrenado.objects.get(pk=modelo_id)
            vacantes = Vacante.objects.filter(modelo_clustering=modelo, grupo=cluster)

            columnas = modelo.columnas_usadas  

            descripcion = ""
            for vacante in vacantes:
                datos = []
                for col in columnas:
                    valor = getattr(vacante, col, None)
                    if valor is not None:
                        datos.append(f"{col.replace('_', ' ').capitalize()}: {valor}")
                descripcion += ", ".join(datos) + "\n"

            targeting = generar_targeting_desde_gemini(descripcion)

            return JsonResponse({ "success": True, **targeting })
        except Exception as e:
            return JsonResponse({ "success": False, "error": str(e) })
    return JsonResponse({ "success": False, "error": "Método no permitido" }, status=405)



