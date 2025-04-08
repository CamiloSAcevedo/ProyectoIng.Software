from django.db import models
from datetime import date

class Campaign(models.Model):
    REDES_SOCIALES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('X', 'X'),
    ]
    
    OBJECTIVES = [
        ('CONVERSIONS', 'Conversiones'),
        ('ENGAGEMENT', 'Interacción'),
        ('BRAND_AWARENESS', 'Conocimiento de marca'),
        ('LEAD_GENERATION', 'Leads'),
    ]

    nombre = models.CharField(max_length=255)
    red_social = models.CharField(max_length=20, choices=REDES_SOCIALES, default='facebook')
    objective = models.CharField(max_length=250, choices=OBJECTIVES, default="REACH")  # Facebook

    #Adicionales (no están en el formulario)
    campaign_id = models.CharField(max_length=255, null=True, blank=True, default="")
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre
    

class AdSet(models.Model):
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
    campaign_id = models.CharField(max_length=250)
    daily_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    billing_event = models.CharField(max_length=250, choices=BILLING_EVENTS, blank=True, default="REACH")  # Facebook
    optimization_goal = models.CharField(max_length=250, choices=OPTIMIZATION_GOALS, blank=True, default="REACH")  # Facebook
    status = models.CharField(max_length=255, blank=True)
    
    #Adicionales (no están en el formulario)
    adset_id= models.CharField(blank=True, max_length=100)
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre

    
class Ad(models.Model):
    REDES_SOCIALES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('X', 'X'),
    ]
    
    adset_id= models.CharField(max_length=100, blank=True)
    creative_id = models.CharField(max_length=250, blank=True)
    red_social = models.CharField(max_length=20, choices=REDES_SOCIALES, default='facebook')
    nombre = models.CharField(max_length=250)
    status = models.CharField(max_length=100, blank=True)

    #Adicionales (no están en el formulario)
    ad_id= models.CharField(blank=True, max_length=100)
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre


class Creative(models.Model):
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
    creative_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre
