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

# Crear una Campaña
def create_campaign():
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"
    params = {
        "name": "Mi campaña automatizada",
        "objective": "LINK_CLICKS",
        "status": "PAUSED",  # Mantén en pausa para evitar gastos accidentales
        "special_ad_categories": [],  # Modifica si es necesario
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    return response.json()

# Crear un Conjunto de Anuncios (AdSet)
def create_adset(campaign_id):
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adsets"
    params = {
        "name": "Mi AdSet",
        "campaign_id": campaign_id,
        "daily_budget": 1000,  # 10 USD por día (mínimo en algunas regiones)
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "REACH",
        "targeting": '{"geo_locations":{"countries":["US"]}}',  # Modifica para tu público objetivo
        "status": "PAUSED",
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    return response.json()

# Crear un Anuncio (Ad)
def create_ad(adset_id, creative_id):
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/ads"
    params = {
        "name": "Mi Anuncio",
        "adset_id": adset_id,
        "creative": f'{{"creative_id":"{creative_id}"}}',
        "status": "PAUSED",
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    return response.json()

# Extraer datos de rendimiento de campañas
def get_campaign_data(campaign_id):
    url = f"{BASE_URL}/{campaign_id}/insights"
    params = {
        "fields": "campaign_name,impressions,clicks,spend",
        "access_token": ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    return response.json()

def get_creative():
    url = f"{BASE_URL}/act_{AD_ACCOUNT_ID}/adcreatives"
    params = {
        "name": "Creative de prueba",
        "title": "¡Oferta de empleo!",
        "body": "Aplica hoy y únete a nuestro equipo.",
        "object_story_spec": "{'link_data': {'link': 'https://tuweb.com', 'message': '¡Oferta de trabajo disponible!'}}",
        "access_token": ACCESS_TOKEN
    }

    response = requests.post(url, data=params)
    print(response.json())  # Esto devuelve el Creative ID

# Ejecutar las funciones
if __name__ == "__main__":
    # Crear una campaña
    campaign = create_campaign()
    print("📌 Campaña creada:", campaign)

    if "id" in campaign:
        campaign_id = campaign["id"]

        # Crear un AdSet
        adset = create_adset(campaign_id)
        print("📌 AdSet creado:", adset)

        if "id" in adset:
            adset_id = adset["id"]

            # ⚠️ Requiere un "Creative ID" previamente creado
            creative_id = "TU_CREATIVE_ID"
            ad = create_ad(adset_id, creative_id)
            print("📌 Anuncio creado:", ad)

            # Extraer métricas de la campaña
            metrics = get_campaign_data(campaign_id)
            print("📌 Métricas de la campaña:", metrics)


def crear_ad(request):
    if request.method == "POST":
        form = AdForm(request.POST)  
        if form.is_valid():
            ad = form.save(commit=False)  
            
            ad.save()  # TO-DO: Eliminar este save para guardarlo cuando ya se haya recibido el id de meta
            messages.success(request, "¡Los datos de ad set se ingresaron exitosamente!")

            return redirect('crear_ad')
        
        else:
            print(ad.errors)
            messages.error(request, "Hubo un error al crear el ad. Revisa los campos.") 

    
    # Limpiar mensajes antes de renderizar la página
    storage = messages.get_messages(request)
    storage.used = True  

    form = AdForm()

    return render(request, 'ad.html', {'form': form})

