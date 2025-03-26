#import tweepy
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
#from django.contrib.auth.decorators import login_required
#from .models import AuthorizedPersonnel
#from .models import Alert
from .forms import CampaignForm, AdSetForm, AdForm
from .models import Campaign, AdSet, Ad
from django. http import JsonResponse 

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
            # Guarda en la base de datos sin el ID de meta
            form.save()  
            messages.success(request, "¡Los datos de campaña se ingresaron exitosamente!")

            # Evita guardarlo aún en la BD para guardar después con ID de meta
            #campaña = form.save(commit=False)  

            # Obtener los datos ingresados por el usuario
            nombre = form.cleaned_data['nombre']
            objective = form.cleaned_data['objective']

            # Construir la URL y parámetros para la API
            url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"
            payload = {
                "name": nombre,
                "objective": objective,
                "status": "PAUSED",  # Para evitar gastos accidentales
                "special_ad_categories": [],  
                "access_token": ACCESS_TOKEN
            }
            '''
            try:
                # Hacer la solicitud POST a la API
                response = requests.post(url, data=payload)

                # Verificar la respuesta de la API
                 if response.status_code == 200 and "id" in respuesta_json:
                    # Asignar el ID de la API de Meta a la campaña en Django
                    campaña.campaign_id = respuesta_json["id"]
                    campaña.save()  # Ahora sí guardamos en la BD

                    messages.success(request, f"✅ Campaña creada exitosamente. ID: {campaña.campaign_id}")
                else:
                    error_msg = respuesta_json.get("error", {}).get("message", "No se pudo crear la campaña")
                    messages.error(request, f"❌ Error al crear la campaña en Meta: {error_msg}")


            except requests.exceptions.RequestException as e:
                messages.error(request, f"🚨 Error en la solicitud: {e}")'
                '''

            return redirect('campaña')  # Redirige después de la solicitud

        else:
            messages.error(request, "Hubo un error al crear la campaña. Revisa los campos.")

    form = CampaignForm()
    return render(request, 'campaña.html', {'form': form})


def mis_campañas(request):
    campañas = Campaign.objects.all()
    return render(request, 'mis_campañas.html', {'campañas':campañas})

# ---------------------- CREAR ADSET META ----------------------#

# Diccionario de Objective -> Optimization Goals permitidos
OPTIMIZATION_GOALS = {
    "BRAND_AWARENESS": ["IMPRESSIONS", "REACH"],
    "ENGAGEMENT": ["POST_ENGAGEMENT", "VIDEO_VIEWS", "IMPRESSIONS", "REACH"],
    "LEAD_GENERATION": ["LEAD_GENERATION", "QUALITY_LEAD", "IMPRESSIONS"],
    "CONVERSIONS": ["CONVERSIONS", "VALUE", "LANDING_PAGE_VIEWS"],
}

def ad_set(request):
    form = AdSetForm()
    return render(request, 'ad_set.html', {'form': form})

def crear_adset(request):
    if request.method == "POST":
        adset = AdSetForm(request.POST)
        if adset.is_valid():
            print("VÁLIDO")
            # Guarda en la base de datos sin el ID de meta
            adset.save()  
            messages.success(request, "¡Los datos de ad set se ingresaron exitosamente!")

            # Evita guardarlo aún en la BD para guardar después con ID de meta
            #adset = form.save(commit=False)  

            '''
            # Verificar que la campaña existe en la BD y tiene un ID en Meta
            campaign = adset.campaign_id
            if not campaign.campaign_id:
                messages.error(request, "❌ La campaña aún no ha sido creada en Meta.")
                return redirect('crear_adset')

            # Obtener los posibles optimization goals según el objective de la campaña
            available_goals = OPTIMIZATION_GOALS.get(campaign.objective, [])
            if adset.optimization_goal not in available_goals:
                messages.error(request, "❌ El Optimization Goal seleccionado no es válido para esta campaña.")
                return redirect('crear_adset')
            '''

            # Datos para la API de Meta
            url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adsets"
            payload = {
                "name": adset.cleaned_data['nombre'],
                "campaign_id": adset.cleaned_data['campaign_id'],
                "daily_budget": adset.cleaned_data['daily_budget'],
                "billing_event": "IMPRESSIONS",  # Se puede hacer dinámico según la necesidad
                "optimization_goal": adset.cleaned_data['optimization_goal'],
                "status": "PAUSED",
                "access_token": ACCESS_TOKEN
            }
            '''
            try:
                response = requests.post(url, json=payload)
                respuesta_json = response.json()

                if response.status_code == 200 and "id" in respuesta_json:
                    adset.adset_id = respuesta_json["id"]
                    adset.save()
                    messages.success(request, f"✅ AdSet creado exitosamente. ID: {adset.adset_id}")
                else:
                    error_msg = respuesta_json.get("error", {}).get("message", "No se pudo crear el AdSet")
                    messages.error(request, f"❌ Error en Meta: {error_msg}")

            except requests.exceptions.RequestException as e:
                messages.error(request, f"🚨 Error en la solicitud: {e}")
            '''
            return redirect('crear_adset')
        
        else:
            messages.error(request, "Hubo un error al crear el adset. Revisa los campos.") 

    # Limpiar mensajes antes de renderizar la página
    storage = messages.get_messages(request)
    storage.used = True  

    form = AdSetForm()
    return render(request, 'ad_set.html', {'form': form})

def mis_adsets(request):
    adsets = AdSet.objects.all()
    return render(request, 'mis_adsets.html', {'adsets': adsets})


def obtener_optimization_goals(request):
    campaign_id = request.GET.get("campaign_id")
    print(f"🔍 Buscando campaign_id: {campaign_id}")  # LOG

    try:
        campaign = Campaign.objects.get(campaign_id=campaign_id)
        print(f"✅ Campaña encontrada: {campaign.nombre}, Objetivo: {campaign.objective}")  # LOG
        optimization_goals = OPTIMIZATION_GOALS.get(campaign.objective, [])
        print(f"🎯 Optimization Goals disponibles: {optimization_goals}")  # LOG

        return JsonResponse({"optimization_goals": optimization_goals})
    except Campaign.DoesNotExist:
        print("❌ Campaña no encontrada")  # LOG
        return JsonResponse({"error": "Campaña no encontrada"}, status=404)


# ---------------------- CREAR ANUNCIO META  ----------------------#
def crear_ad(request):
    if request.method == "POST":
        form = AdForm(request.POST)
        if form.is_valid():
            anuncio = form.save(commit=False)

            # Verificar que el AdSet exista en la BD
            if not anuncio.adset.adset_id:
                messages.error(request, "❌ El AdSet aún no ha sido creado en Meta.")
                return redirect('crear_ad')

            # Datos para la API de Meta
            url = f"{BASE_URL}/{AD_ACCOUNT_ID}/ads"
            payload = {
                "name": anuncio.nombre,
                "adset_id": anuncio.adset.adset_id,
                "status": "PAUSED",
                "creative": {"creative_id": anuncio.creative_id},  # Debes haber creado el Creative antes
                "access_token": ACCESS_TOKEN
            }

            '''
            try:
                response = requests.post(url, data=payload)
                respuesta_json = response.json()

                if response.status_code == 200 and "id" in respuesta_json:
                    anuncio.ad_id = respuesta_json["id"]
                    anuncio.save()
                    messages.success(request, f"✅ Anuncio creado. ID: {anuncio.ad_id}")
                else:
                    error_msg = respuesta_json.get("error", {}).get("message", "No se pudo crear el anuncio")
                    messages.error(request, f"❌ Error en Meta: {error_msg}")

            except requests.exceptions.RequestException as e:
                messages.error(request, f"🚨 Error en la solicitud: {e}")
            '''

            return redirect('crear_ad')

    else:
        form = AdSetForm()  # Asegurar que se pase un formulario vacío si es GET

    return render(request, 'ad_set.html', {'form': form})



def ad(request):
    return render(request, 'ad.html')
