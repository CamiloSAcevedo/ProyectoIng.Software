import tweepy
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
#from .models import AuthorizedPersonnel
#from .models import Alert
from .forms import CampaignForm, AdSetForm, AdForm, CreativeForm, VacanteForm, UploadFileForm
from .models import Campaign, AdSet, Ad, Creative, Vacante, Post
from .models import Campaign, AdSet, Ad, Creative, Vacante, Post
from django. http import JsonResponse 
import requests
import os
from dotenv import load_dotenv
from django.contrib.auth.decorators import user_passes_test
from .utils.ai import generar_message_creative, generar_body_creative
from django.urls import reverse

import pandas as pd
from django.db import IntegrityError


# Cargar variables desde el .env
load_dotenv()

# Verificar que el usuario es staff (administrador)
def es_staff(user):
    return user.is_authenticated and user.is_staff

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

@login_required
@login_required
def estadisticas(request):
    return render(request, 'estadisticas.html')

#@login_required
def crear_ads(request):
    return render(request, 'crear_ads.html')

#def vacantes(request):
   # return render(request, 'mis_vacantes.html')

#---------------------- KEYS API X ----------------------#

client = tweepy.Client(
    consumer_key=settings.TWITTER_API_KEY,
    consumer_secret=settings.TWITTER_API_SECRET,
    access_token=settings.TWITTER_ACCESS_TOKEN,
    access_token_secret=settings.TWITTER_ACCESS_SECRET
)


#---------------------- APROBACIÓN O RECHAZO ADS ----------------------#
#Vista para listar anuncios pendientes
@user_passes_test(lambda u: u.is_staff)
def revisar_contenido_pendiente(request, tipo):
    MODELOS = {
        'ad': Ad,
        'post': Post,
    }

    Modelo = MODELOS.get(tipo)
    if not Modelo:
        messages.error(request, "Tipo de contenido inválido.")
        return redirect("home")  # o donde corresponda

    contenido_pendiente = Modelo.objects.filter(revision__estado="Pendiente")

    return render(request, "contenido_pendiente.html", {
        "contenidoo": contenido_pendiente,
        "tipo": tipo
    })


# Vista para actualizar estado y comentario (nuevo)
# Se llama con actualizar_estado_contenido
@user_passes_test(lambda u: u.is_staff)
def aprobar_contenido(request, tipo, objeto_id):
    MODELOS = {
        'ad': Ad,
        'post': Post,
    }

    Modelo = MODELOS.get(tipo)
    if not Modelo:
        messages.error(request, "Tipo de contenido inválido.")
        return redirect("revisar_contenido_pendiente")

    objeto = get_object_or_404(Modelo, pk=objeto_id)

    if not hasattr(objeto, 'revision') or objeto.revision is None:
        messages.error(request, f"Este {tipo} no tiene una revisión asociada.")
        #return redirect("revisar_contenido_pendiente")
        return redirect(reverse('revisar_contenido_pendiente', kwargs={'tipo':tipo}))


    revision = objeto.revision
# Vista para actualizar estado y comentario (nuevo)
# Se llama con actualizar_estado_contenido
@user_passes_test(lambda u: u.is_staff)
def aprobar_contenido(request, tipo, objeto_id):
    MODELOS = {
        'ad': Ad,
        'post': Post,
    }

    Modelo = MODELOS.get(tipo)
    if not Modelo:
        messages.error(request, "Tipo de contenido inválido.")
        return redirect("revisar_contenido_pendiente")

    objeto = get_object_or_404(Modelo, pk=objeto_id)

    if not hasattr(objeto, 'revision') or objeto.revision is None:
        messages.error(request, f"Este {tipo} no tiene una revisión asociada.")
        #return redirect("revisar_contenido_pendiente")
        return redirect(reverse('revisar_contenido_pendiente', kwargs={'tipo':tipo}))


    revision = objeto.revision

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        comentario = request.POST.get("comentario")

        revision.estado = nuevo_estado
        revision.comentario_admin = comentario
        revision.estado = nuevo_estado
        revision.comentario_admin = comentario

        try:
            if nuevo_estado == "Aprobado":
                if tipo == "ad":
                    if(crear_ad_meta(request, objeto)):
                        messages.success(request, "Anuncio aprobado y publicado en Meta.")
                    else:
                        messages.success(request, "Hubo un error en la creación del anuncio.")
                        revision.estado = "Rechazado"
                elif tipo == "post":
                    # Solo para posts: publicar en X (Twitter)
                    #client.create_tweet(text=objeto.nombre)  # o texto, según tu modelo
                    messages.success(request, "Post aprobado y publicado en X (Twitter).")
                    messages.success(request, "Publicación aprobada.")
                if tipo == "ad":
                    if(crear_ad_meta(request, objeto)):
                        messages.success(request, "Anuncio aprobado y publicado en Meta.")
                    else:
                        messages.success(request, "Hubo un error en la creación del anuncio.")
                        revision.estado = "Rechazado"
                elif tipo == "post":
                    # Solo para posts: publicar en X (Twitter)
                    #client.create_tweet(text=objeto.nombre)  # o texto, según tu modelo
                    messages.success(request, "Post aprobado y publicado en X (Twitter).")
                    messages.success(request, "Publicación aprobada.")
            else:
                messages.success(request, "Estado actualizado.")
        except Exception as e:
            messages.error(request, f"Error en la acción de publicación: {str(e)}")

        revision.save()
        return redirect(reverse('revisar_contenido_pendiente', kwargs={'tipo': tipo}))

    return render(request, "aprobar_contenido.html", {"objeto": objeto, "tipo": tipo})

# Vista para listar estado anuncios (usuario normal)
@login_required
def mis_solicitudes_contenido(request, tipo):
    MODELOS = {
        'ad': Ad,
        'post': Post,
    }

    Modelo = MODELOS.get(tipo)
    if not Modelo:
        messages.error(request, "Tipo de contenido inválido.")
        return redirect("home")  # o donde corresponda
    
    estado = request.GET.get('estado')

    if not estado:  # Si no se seleccionó estado o es vacío, traer todos
        contenido_pendiente = Modelo.objects.filter(revision__usuario=request.user)
    else:
        contenido_pendiente = Modelo.objects.filter(revision__usuario=request.user, revision__estado=estado)

    return render(request, "mis_solicitudes_contenido.html", {
        "contenidoo": contenido_pendiente,
        "tipo": tipo,
        "estado_seleccionado": estado  # para mantener seleccionado en el HTML
    })

    


# ---------------------- API DE X ----------------------#
# Configurar autenticación con Tweepy
# Autenticación con la API v2

@login_required
def crear_post(request):
    if request.method == "POST":
        tweet_text = request.POST.get("tweet")
        if tweet_text:
            try:
                #client.create_tweet(text=tweet_text)  # Publica el tweet
                #messages.success(request, "¡Tweet publicado correctamente!")
                #ad = Ad.objects.create(texto=tweet_text, usuario= request.user)
                # Crear la revisión asociada al usuario autenticado
                revision = Revision.objects.create(
                    usuario=request.user,  # Usuario que está haciendo el request
                    estado='Pendiente',    # Estado inicial
                )
                post = Post.objects.create(texto=tweet_text, revision=revision)
                messages.success(request, "¡El anuncio fue enviado para aprobación!")
            except Exception as e:
                messages.error(request, f"Error al publicar el tweet: {str(e)}")

        return redirect("crear_post")  # Redirecciona a la misma página
    vacantes = Vacante.objects.all() #Necesario para el autocompletar
                                              #  Necesario para el autocompletar
    return render(request, "crear_post.html", {"vacantes": vacantes})


# ---------------------- CREAR CAMPAÑA META ----------------------#
def campaña(request):
    if request.method == "POST":
        form = CampaignForm(request.POST) 
    else:
        form = CampaignForm()

    return render(request, 'campaña.html', {'form': form})

def crear_campaña(request):
    if request.method == "POST":
        form = CampaignForm(request.POST)
        if form.is_valid():
            # Guarda en la base de datos sin el ID de meta
            campaña = form.save(commit=False)  
            campaña.plataforma = form.cleaned_data['plataforma']
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
                response = requests.post(url, json=payload)
                respuesta_json = response.json()


                # Verificar la respuesta de la API
                if response.status_code == 200 and "id" in respuesta_json:
                    # Asignar el ID de la API de Meta a la campaña en Django
                    campaña.campaign_id = respuesta_json["id"]
                    campaña.save()  # Ahora sí guardamos en la BD

                    messages.success(request, f"✅ Campaña creada exitosamente. ID: {campaña.campaign_id}")
                else:
                    error_msg = respuesta_json.get("error", {}).get("message", "No se pudo crear la campaña")
                    messages.error(request, f"❌ Error al crear la campaña en Meta: {error_msg}")
                    print(error_msg)


            except requests.exceptions.RequestException as e:
                messages.error(request, f"🚨 Error en la solicitud: {e}")
                #'''

            return redirect('campaña')  # Redirige después de la solicitud

        else:
            messages.error(request, "Hubo un error al crear la campaña. Revisa los campos.")

    form = CampaignForm()
    return render(request, 'campaña.html', {'form': form})


def mis_campañas(request):
    plataforma = request.session.get('plataforma', )
    campañas = Campaign.objects.filter(plataforma=plataforma)
    return render(request, 'mis_campañas.html', {'campañas':campañas})


def set_plataforma(request):
    plataforma = request.GET.get('plataforma')
    if plataforma in ['facebook', 'instagram']:
        request.session['plataforma'] = plataforma
        return JsonResponse({'ok': True})
    return JsonResponse({'error': 'Plataforma inválida'}, status=400)

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
                campaign = Campaign.objects.get(nombre=adset.campaign_id)
            except Campaign.DoesNotExist:
                messages.error(request, "❌ La campaña aún no ha sido creado en Meta.")
                return redirect('crear_adset')

            adset.save()  # TO-DO: Eliminar este save para guardarlo cuando ya se haya recibido el id de meta
            messages.success(request, "¡Los datos de ad set se ingresaron exitosamente!")

            # Datos para la API de Meta
            url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adsets"
            payload = {
                "name": adset.nombre,
                "campaign_id": adset.campaign_id.campaign_id,
                "daily_budget": int(adset.daily_budget),
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
            #'''
            return redirect('crear_adset')
        
        else:
            messages.error(request, "Hubo un error al crear el adset. Revisa los campos.") 

    # Limpiar mensajes antes de renderizar la página
    storage = messages.get_messages(request)
    storage.used = True  

    form = AdSetForm()
    return render(request, 'ad_set.html', {'form': form})

def mis_adsets(request):
    plataforma = request.session.get('plataforma')
    adsets = AdSet.objects.filter(plataforma=plataforma)
    return render(request, 'mis_adsets.html', {'adsets': adsets})


def obtener_optimization_goals(request):
    campaign_id = request.GET.get("campaign_id")
    print(f"🔍 Buscando campaign_id: {campaign_id}")  # LOG

    try:
        campaign = Campaign.objects.get(id=campaign_id)
        print(f"✅ Campaña encontrada: {campaign.nombre}, Objetivo: {campaign.objective}")  # LOG
        optimization_goals = OPTIMIZATION_GOALS.get(campaign.objective, [])
        print(f"🎯 Optimization Goals disponibles: {optimization_goals}")  # LOG

        return JsonResponse({"optimization_goals": optimization_goals})
    except Campaign.DoesNotExist:
        print("❌ Campaña no encontrada")  # LOG
        return JsonResponse({"error": "Campaña no encontrada"}, status=404)



# ---------------------- CREAR ANUNCIO META  ----------------------#

def ad(request):
    form = AdForm()
    return render(request, 'ad.html', {'form': form})

from administrador.models import Revision  # Asegúrate de importar el modelo Revision

def crear_ad(request):
    if request.method == "POST":
        form = AdForm(request.POST)  
        if form.is_valid():
            ad = form.save(commit=False)

            # Crear la revisión asociada al usuario autenticado
            revision = Revision.objects.create(
                usuario=request.user,  # Usuario que está haciendo el request
                estado='Pendiente',    # Estado inicial
            )

            # Asignar la revisión al anuncio
            ad.revision = revision

            # Guardar el anuncio (con la revisión asignada)
            ad.save()

            messages.success(request, "¡Los datos del ad se ingresaron exitosamente y se enviaron para ser revisados!")

            return redirect('crear_ad')

        else:
            print(form.errors)
            messages.error(request, "Hubo un error al crear el ad. Revisa los campos.") 

    # Limpiar mensajes antes de renderizar la página
    storage = messages.get_messages(request)
    storage.used = True  

    form = AdForm()
    return render(request, 'ad.html', {'form': form})


def crear_ad_meta(request, ad):
    print("Se llamó la función de crear_ad_meta")
    return True
    '''
     # Datos para la API de Meta
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/ads"
    payload = {
        "name": ad.nombre,
        "adset_id": ad.adset_id,
        "status": "PAUSED",
        "creative": {"creative_id": ad.creative_id},  # Debes haber creado el Creative antes
        "access_token": ACCESS_TOKEN
    }
    
    try:
        response = requests.post(url, data=payload)
        respuesta_json = response.json()

        if response.status_code == 200 and "id" in respuesta_json:
            ad.ad_id = respuesta_json["id"]
            ad.save()
            messages.success(request, f"✅ Anuncio creado. ID: {ad.ad_id}")
            return True
        else:
            error_msg = respuesta_json.get("error", {}).get("message", "No se pudo crear el anuncio")
            messages.error(request, f"❌ Error en Meta: {error_msg}")
            return False
    except requests.exceptions.RequestException as e:
        messages.error(request, f"🚨 Error en la solicitud: {e}")
    '''
            

def mis_ads(request):
    plataforma = request.session.get('plataforma')
    ads = Ad.objects.filter(plataforma=plataforma)
    return render(request, 'mis_ads.html', {'ads': ads})

# ---------------------- GENERAR TEXTO CON IA PARA CREATIVES----------------------#
# para búsqueda de vacantes

def buscar_vacante(request):
    q = request.GET.get("q", "")
    resultados = Vacante.objects.filter(vacante__icontains=q)[:10]
    data = [{"id": v.id, "vacante": v.vacante} for v in resultados]
    return JsonResponse(data, safe=False)




def generar_message_ia(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        vacante_id = request.POST.get("vacante_id")

        vacante_info = ""
        if vacante_id:
            try:
                vacante = Vacante.objects.get(id=vacante_id)
                vacante_info = f"""
                Vacante: {vacante.vacante}
                Empresa: {vacante.empresa}
                Ubicación: {vacante.ubicacion}
                Modalidad: {vacante.modalidad}
                Salario: {vacante.salario}
                Experiencia: {vacante.experiencia}
                Descripción: {vacante.descripcion}
                """
            except Vacante.DoesNotExist:
                pass

        texto = generar_message_creative(prompt, vacante_info)
        return JsonResponse({"texto": texto})

def generar_body_ia(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        vacante_id = request.POST.get("vacante_id")

        vacante_info = ""
        if vacante_id:
            try:
                vacante = Vacante.objects.get(id=vacante_id)
                vacante_info = f"""
                Vacante: {vacante.vacante}
                Empresa: {vacante.empresa}
                Ubicación: {vacante.ubicacion}
                Modalidad: {vacante.modalidad}
                Salario: {vacante.salario}
                Experiencia: {vacante.experiencia}
                Descripción: {vacante.descripcion}
                """
            except Vacante.DoesNotExist:
                pass

        texto = generar_body_creative(prompt, vacante_info)
        return JsonResponse({"texto": texto})


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

            if response.status_code == 200 and "id" in data:
                creative.creative_id = data["id"]
                creative.save()
                messages.success(request, f"Creative creado con ID: {creative.creative_id}")
                return redirect("crear_creative")  # Redirige a la página de éxito
            else:
                error_msg = data.get("error", {}).get("message", "Error desconocido")
                messages.error(request, f"Error en Meta: {error_msg}")
            
            #'''
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
    plataforma = request.session.get('plataforma')
    creatives = Creative.objects.filter(plataforma = plataforma)
    return render(request, 'mis_creatives.html', {'creatives':creatives})

# ---------------------- VER MIS VACANTES ----------------------#

def mis_vacantes(request):
    if request.method == 'POST':
        # Obtén los datos del formulario
        vacante = request.POST.get('vacante')
        empresa = request.POST.get('empresa')
        ubicacion = request.POST.get('ubicacion')
        contrato = request.POST.get('contrato')
        salario = request.POST.get('salario')
        descripcion = request.POST.get('descripcion')

        # Verifica que todos los campos obligatorios estén completos
        if not all([vacante, empresa, ubicacion, contrato, salario]):
            return render(request, 'mis_vacantes.html', {
                'error': 'Por favor, completa todos los campos obligatorios.',
                'vacantes': Vacante.objects.all()
            })

        # Guarda la nueva vacante en la base de datos
        Vacante.objects.create(
            vacante=vacante,
            empresa=empresa,
            ubicacion=ubicacion,
            contrato=contrato,
            salario=salario,
            descripcion=descripcion
        )
        return redirect('vacantes')  # Redirige a la misma página después de guardar

    # Manejar la búsqueda de vacantes
    query = request.GET.get('q')  # Obtén el término de búsqueda del parámetro 'q'
    if query:
        # Filtrar las vacantes que coincidan con el término de búsqueda
        vacantes = Vacante.objects.filter(
            Q(vacante__icontains=query) |
            Q(empresa__icontains=query) |
            Q(ubicacion__icontains=query)
            #Q(grupo__icontains=query)   # Buscar en el campo 'grupo'
        )
    else:
        # Si no hay término de búsqueda, muestra todas las vacantes
        vacantes = Vacante.objects.all()

    return render(request, 'mis_vacantes.html', {'vacantes': vacantes})



def cargar_excel(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo_excel')
        if archivo:
            df = pd.read_excel(archivo)  #  pd.read_csv(archivo) si es CSV
            for _, row in df.iterrows():
                Vacante.objects.create(
                    vacante=row['vacante'],
                    empresa=row['empresa'],
                    ubicacion=row['ubicacion'],
                    contrato=row['contrato'],
                    salario=row['salario'],
                    descripcion=row.get('descripcion', ''),
                    industria=row.get('industria', ''),
                    modalidad=row.get('modalidad', ''),
                    experiencia=row.get('experiencia', '')
                )
        return redirect('vacantes')
    
# ---------------------------- AUTO RELLENO EN POST --------------------------------#

def obtener_vacante(request, vacante_id):
    try:
        vacante = Vacante.objects.get(id=vacante_id)
        return JsonResponse({
            'vacante': vacante.vacante or "",
            'empresa': vacante.empresa or "",
            'ubicacion': vacante.ubicacion or "",
            'contrato': vacante.contrato or "",
            'salario': vacante.salario or "",
            'descripcion': vacante.descripcion or ""
        })
    except Vacante.DoesNotExist:
        return JsonResponse({'error': 'Vacante no encontrada'}, status=404)
