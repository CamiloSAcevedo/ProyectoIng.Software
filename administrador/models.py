from django.db import models
from datetime import date
from django.contrib.auth.models import User

# ---------------------- TABLA PARA REVISIÓN DE ADMINISTRADOR----------------------#
class Revision(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revisiones')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    comentario_admin = models.TextField(blank=True, null=True, help_text="Comentario del administrador al aprobar o rechazar")
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return f"Revisión por {self.usuario} - {self.estado}"
    
# ---------------------- MODELOS X ----------------------#
class Post(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]
    
    nombre = models.CharField(max_length=250)
    status = models.CharField(max_length=100, blank=True)
    texto = models.TextField(blank=True, null=True)  # Texto del anuncio
    revision = models.OneToOneField(Revision, on_delete=models.CASCADE, null=True, blank=True) # Campo para aprovación
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.texto

# ---------------------- MODELOS META ----------------------#
class Campaign(models.Model):
    # Keys
    campaign_id = models.CharField(max_length=255, blank=True, default="") 
    
    OBJECTIVES = [
        ('CONVERSIONS', 'Conversiones'),
        ('POST_ENGAGEMENT', 'Interacción'),
        ('BRAND_AWARENESS', 'Conocimiento de marca'),
        ('LEAD_GENERATION', 'Leads'),
    ]

    nombre = models.CharField(max_length=255)
    objective = models.CharField(max_length=250, choices=OBJECTIVES, default="REACH") 

    #Adicionales (no están en el formulario)
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre
    

class AdSet(models.Model):
    # Keys 
    adset_id= models.CharField(blank=True, max_length=100) 
    campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE) # FK

    #añadir campo targeting
    BILLING_EVENTS = [
        ('IMPRESSIONS', 'CPM (Por cada 1000 impresiones)'),
        ('CLICKS', 'CPC (Por cada click)'),
        ('LINK_CLICKS', 'Clicks en enlaces específicos'),
        ('POST_ENGAGEMENT', 'Interacciones'),
        ('VIDEO_VIEWS', 'Vistas de video'),
    ]
    OPTIMIZATION_GOALS = [
        ('IMPRESSIONS', 'Conversiones'),
        ('REACH', 'Alcance'),
        ('POST_ENGAGEMENT', 'Engagement con el post'),
        ('VIDEO_VIEWS', 'Vistas'),
        ('IMPRESSIONS', 'Impresiones'),
        ('LEAD_GENERATION', 'Leads'),
        ('CONVERSIONS', 'Conversiones'),
        ('VALUE', 'Value'),
        ('LANDING_PAGE_VIEWS', 'Landing page'),
    ]

    nombre = models.CharField(max_length=255)
    daily_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    billing_event = models.CharField(max_length=250, choices=BILLING_EVENTS, blank=True, default="REACH") 
    optimization_goal = models.CharField(max_length=250, choices=OPTIMIZATION_GOALS, blank=True, default="REACH")  
    status = models.CharField(max_length=255, blank=True)
    
    #Adicionales (no están en el formulario
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre

class Creative(models.Model):
    # Keys
    creative_id = models.CharField(max_length=100, blank=True) 

    nombre = models.CharField(max_length=255) # Nombre interno para identificación en la API
    name = models.CharField(max_length=255) # Título visible en el anuncio
    message = models.TextField(blank=True, null=True)  # Capta la atención inicial, PRINCIPAL
    body = models.TextField(blank=True, null=True)  # Da un poco mas de contexto 
    image_url = models.URLField(blank=True, null=True)  # Imagen del anuncio
    link = models.URLField(blank=True, null=True)  # URL del enlace al que redirige el anuncio
    call_to_action = models.CharField(max_length=50, choices=[
        ("LEARN_MORE", "Más información"),
        ("SIGN_UP", "Registrarse"),
        ("SHOP_NOW", "Comprar ahora"),
        ("CONTACT_US", "Contáctanos"),
        ("SUBSCRIBE", "Suscribirse"),
        ("GET_OFFER", "Obtener oferta"),
    ])

    #Adicionales (no están en el formulario)
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre
    

class Ad(models.Model):
    #Keys
    ad_id= models.CharField(blank=True, max_length=100) 
    adset_id = models.ForeignKey(AdSet, on_delete=models.CASCADE) # FK
    creative_id = models.ForeignKey(Creative, on_delete=models.CASCADE) # FK

    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]
    
    nombre = models.CharField(max_length=250)
    status = models.CharField(max_length=100, blank=True)

    revision = models.OneToOneField(Revision, on_delete=models.CASCADE, null=True, blank=True) # Campo para aprovación
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre
    

# ---------------------- VACANTES ----------------------#
class Vacante(models.Model):
    vacante = models.CharField(max_length=255)
    empresa = models.TextField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    contrato = models.CharField(max_length=100)
    salario = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    industria = models.CharField(max_length=100, null=True)
    modalidad = models.CharField(max_length=50, choices=[('Remoto', 'Remoto'), ('Presencial', 'Presencial'), ('Híbrido', 'Híbrido')], null=True)
    experiencia = models.CharField(max_length=100, null=True)
    grupo = models.IntegerField(null=True, blank=True) # Para clustering

    def __str__(self):
        return self.vacante
    
# ---------------------- MODELOS TIKTOK ---------------------- #
class AdvertiserTikTok(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class CampaignTikTok(models.Model):
    advertiser = models.ForeignKey(AdvertiserTikTok, on_delete=models.CASCADE, related_name='campaigns')
    nombre = models.CharField(max_length=100)
    objetivo = models.CharField(max_length=100)
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class AdGroupTikTok(models.Model):
    campaign = models.ForeignKey(CampaignTikTok, on_delete=models.CASCADE, related_name='adgroups')
    nombre = models.CharField(max_length=100)
    segmentacion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class AdTikTok(models.Model):
    adgroup = models.ForeignKey(AdGroupTikTok, on_delete=models.CASCADE, related_name='ads')
    nombre = models.CharField(max_length=100)
    contenido = models.TextField()
    url = models.URLField(blank=True)
    imagen = models.ImageField(upload_to='tiktok_ads_images/', null=True, blank=True)
    # ...otros campos...

    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
        ('PUBLICADO', 'Publicado'),
    ]
    
    status = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    comentario_admin = models.TextField(blank=True, null=True)

    revision = models.OneToOneField(Revision, on_delete=models.CASCADE, null=True, blank=True) # Campo para aprovación
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre
    

# ----------------------------------------------------#