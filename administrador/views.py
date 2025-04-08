import tweepy
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
#from django.contrib.auth.decorators import login_required
#from .models import AuthorizedPersonnel
#from .models import Alert
from .forms import CampaignForm, AdSetForm, AdForm, CreativeForm
from .models import Campaign, AdSet, Ad, Creative
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
PAGE_ID = os.getenv("PAGE_ID")

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


# ---------------------- CREAR CAMPAÑA META ----------------------#
def campaña(request):
    red_social = ""  # Valor por defecto

    if request.method == "POST":
        red_social = request.POST.get("red_social", "")  # Captura la red social del formulario
        form = CampaignForm(request.POST, red_social=red_social)  # Pasa red_social al formulario
    else:
        form = CampaignForm()

    return render(request, 'campaña.html', {'form': form, 'red_social': red_social})

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
        form = AdSetForm(request.POST)
        if form.is_valid():
            adset = form.save(commit=False)

            # Verificar que la campaña existe en la BD y tiene un ID en Meta
            try:
                campaign = Campaign.objects.get(campaign_id=adset.campaign_id)
            except Campaign.DoesNotExist:
                messages.error(request, "❌ La campaña aún no ha sido creado en Meta.")
                return redirect('crear_adset')

            adset.save()  # TO-DO: Eliminar este save para guardarlo cuando ya se haya recibido el id de meta
            messages.success(request, "¡Los datos de ad set se ingresaron exitosamente!")

            # Datos para la API de Meta
            url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adsets"
            payload = {
                "name": adset.nombre,
                "campaign_id": adset.campaign_id,
                "daily_budget": adset.daily_budget,
                "billing_event": adset.billing_event,  # Se puede hacer dinámico según la necesidad
                "optimization_goal": adset.optimization_goal,
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
def ad(request):
    red_social = ""  # Valor por defecto

    if request.method == "POST":
        red_social = request.POST.get("red_social", "")  # Captura la red social del formulario
        form = AdForm(request.POST, red_social=red_social)  # Pasa red_social al formulario
    else:
        form = AdForm()

    return render(request, 'ad.html', {'form': form, 'red_social': red_social})

def crear_ad(request):
    if request.method == "POST":
        form = AdForm(request.POST)  
        if form.is_valid():
            ad = form.save(commit=False)  
            
            # Confirmación de que existe el adset
            try:
                adset = AdSet.objects.get(adset_id=ad.adset_id)
            except AdSet.DoesNotExist:
                messages.error(request, "❌ El AdSet aún no ha sido creado en Meta.")
                return redirect('crear_ad')
            
            # Confirmación de que existe el creative
            try:
                creative = Creative.objects.get(creative_id=ad.creative_id)
            except Creative.DoesNotExist:
                messages.error(request, "❌ El Creative aún no ha sido creado en Meta.")
                return redirect('crear_ad')
            
            ad.save()  # TO-DO: Eliminar este save para guardarlo cuando ya se haya recibido el id de meta
            messages.success(request, "¡Los datos de ad set se ingresaron exitosamente!")

            # Datos para la API de Meta
            url = f"{BASE_URL}/{AD_ACCOUNT_ID}/ads"
            payload = {
                "name": ad.nombre,
                "adset_id": ad.adset_id,
                "status": "PAUSED",
                "creative": {"creative_id": ad.creative_id},  # Debes haber creado el Creative antes
                "access_token": ACCESS_TOKEN
            }

            '''
            try:
                response = requests.post(url, data=payload)
                respuesta_json = response.json()

                if response.status_code == 200 and "id" in respuesta_json:
                    ad.ad_id = respuesta_json["id"]
                    ad.save()
                    messages.success(request, f"✅ Anuncio creado. ID: {ad.ad_id}")
                else:
                    error_msg = respuesta_json.get("error", {}).get("message", "No se pudo crear el anuncio")
                    messages.error(request, f"❌ Error en Meta: {error_msg}")

            except requests.exceptions.RequestException as e:
                messages.error(request, f"🚨 Error en la solicitud: {e}")
            '''

            return redirect('crear_ad')
        
        else:
            print(ad.errors)
            messages.error(request, "Hubo un error al crear el ad. Revisa los campos.") 

    
    # Limpiar mensajes antes de renderizar la página
    storage = messages.get_messages(request)
    storage.used = True  

    form = AdForm()

    return render(request, 'ad.html', {'form': form})

def mis_ads(request):
    ads = Ad.objects.all()
    return render(request, 'mis_ads.html', {'ads': ads})

# ---------------------- CREAR CREATIVE META  ----------------------#

def crear_creative(request):
    if request.method == "POST":
        form = CreativeForm(request.POST)

        if form.is_valid():
            creative = form.save(commit=False)  
            creative.save()  # TO-DO: Eliminar este save para guardarlo cuando ya se haya recibido el id de meta
            print("se salvaron los datos")
            messages.success(request, "¡Los datos del creative set se ingresaron exitosamente!")

            # Construir payload para la API de Meta
            payload = {
                "name": creative.nombre,  # Nombre interno para identificación en la API
                "body": creative.body or "", # Cuerpo del anuncio
                "object_story_spec": {
                    "page_id": PAGE_ID,
                    "link_data": {
                        "message": creative.message, # Mensaje principal
                        "name": creative.name,  # Título visible en el anuncio
                        "image_url": creative.image_url,
                        "call_to_action": {
                            "type": creative.call_to_action,
                            "value": {
                                "link": creative.link # Enlace al que redirijirá el anuncio
                            }
                        }
                    }
                },
                "access_token": ACCESS_TOKEN
            }

            return render(request, "creative.html", {"form": form, "creative":creative})

            '''
            # Enviar solicitud a Meta para crear el Creative
            url = f"{BASE_URL}/act_{AD_ACCOUNT_ID}/adcreatives"
            response = requests.post(url, json=payload)
            data = response.json()

            if "id" in data:
                creative.creative_id = data["id"]
                creative.save()
                messages.success(request, f"Creative creado con ID: {creative.creative_id}")
                return redirect("crear_creative")  # Redirige a la página de éxito
            else:
                error_msg = data.get("error", {}).get("message", "Error desconocido")
                messages.error(request, f"Error en Meta: {error_msg}")
            
            '''
        else:
            print(form.errors)
            messages.error(request, "Hubo un error al crear el adset. Revisa los campos.")

    else:
        form = CreativeForm()

    # Limpiar mensajes antes de renderizar la página
    storage = messages.get_messages(request)
    storage.used = True  

    form = CreativeForm()

    return render(request, "creative.html", {"form": form})

def mis_creatives(request):
    creatives = Creative.objects.all()
    return render(request, 'mis_creatives.html', {'creatives':creatives})

