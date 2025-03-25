#import tweepy
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
#from django.contrib.auth.decorators import login_required
#from .models import AuthorizedPersonnel
#from .models import Alert
from .forms import CampaignForm
from .models import Campaign

import requests
import os
from dotenv import load_dotenv

# Cargar variables desde el .env
load_dotenv()

# Obtener valores

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("ADD_ACCOUNT_ID")
API_VERSION = os.getenv("API_VERSION")
BASE_URL = os.getenv("BASE_URL")

# Create your views here.
#@login_required esto es de autenticacion

def panel(request):
    return render(request, 'panel.html')

#@login_required
def estadisticas(request):
    return render(request, 'estadisticas.html')

#@login_required
def crear_ads(request):
    return render(request, 'crear_ads.html')


'''
# ---------------------- API DE X ----------------------#
# Configurar autenticación con Tweepy
# Autenticación con la API v2
client = tweepy.Client(
    consumer_key=settings.TWITTER_API_KEY,
    consumer_secret=settings.TWITTER_API_SECRET,
    access_token=settings.TWITTER_ACCESS_TOKEN,
    access_token_secret=settings.TWITTER_ACCESS_SECRET
)

#@login_required
def crear_ads(request):
    if request.method == "POST":
        tweet_text = request.POST.get("tweet")
        if tweet_text:
            try:
                client.create_tweet(text=tweet_text)  # Publica el tweet
                messages.success(request, "¡Tweet publicado correctamente!")
            except Exception as e:
                messages.error(request, f"Error al publicar el tweet: {str(e)}")

        return redirect("crear_ads")  # Redirecciona a la misma página
    
    return render(request, "crear_ads.html")
'''

# ---------------------- DEFINICIÓN CAMPAÑAS ----------------------#
def campaña(request):
    red_social = ""  # Valor por defecto

    if request.method == "POST":
        red_social = request.POST.get("red_social", "")  # Captura la red social del formulario
        form = CampaignForm(request.POST, red_social=red_social)  # Pasa red_social al formulario
    else:
        form = CampaignForm()

    return render(request, 'campaña.html', {'form': form, 'red_social': red_social})


# ---------------------- CREAR CAMPAÑA META ----------------------#
def crear_campaña(request):
    if request.method == "POST":
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda en la base de datos
            messages.success(request, "¡Los datos de campaña se ingresaron exitosamente!")  # ✅ Agregar mensaje de éxito

            # Obtener los datos ingresados por el usuario
            nombre = form.cleaned_data['nombre']
            objective = form.cleaned_data['objective']
            red_social = form.cleaned_data['red_social']


            url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"
            params = {
                "name": nombre,
                "objective":objective,
                "status": "PAUSED",  # Mantén en pausa para evitar gastos accidentales
                "special_ad_categories": [],  # Modifica si es necesario
                "access_token": ACCESS_TOKEN
            }
            #response = requests.post(url, params=params)
            #return response.json()

            print(url, params)

            '''
            try:
                # Hacer la solicitud POST a la API
                response = requests.post(BASE_URL, json=payload)

                # Verificar la respuesta de la API
                if response.status_code == 201:
                    mensaje = "✅ Campaña creada exitosamente."
                else:
                    mensaje = f"❌ Error: {response.json().get('message', 'No se pudo crear la campaña')}"
            except requests.exceptions.RequestException as e:
                mensaje = f"🚨 Error en la solicitud: {e}"
                '''

            return redirect('campaña')  # Redirige para mostrar el mensaje
        
        else:
            messages.error(request, "Hubo un error al crear la campaña. Revisa los campos.")  # ✅ Mensaje de error

    form = CampaignForm()
    return render(request, 'campaña.html', {'form': form})
    #return render(request, 'campaña.html', {'form': form, 'red_social': red_social})


def campañas_creadas(request):
    campañas = Campaign.objects.all()
    return render(request, 'campañas_creadas.html', {'campañas':campañas})

def ad_set(request):
    return render(request, 'ad_set.html')

def ad(request):
    return render(request, 'ad.html')
