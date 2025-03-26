from django.db import models
from datetime import date

class Campaign(models.Model):
    REDES_SOCIALES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
    ]
    
    OBJECTIVES = [
        ('CONVERSIONS', 'Conversiones'),
        ('ENGAGEMENT', 'Interacción'),
        ('BRAND_AWARENESS', 'Conocimiento de marca'),
        ('LEAD_GENERATION', 'Leads'),
    ]

    nombre = models.CharField(max_length=255)
    red_social = models.CharField(max_length=20, choices=REDES_SOCIALES, default='facebook')
    formato = models.CharField(max_length=255, blank=True, null=True)
    objective = models.CharField(max_length=250, choices=OBJECTIVES, blank=True, default="REACH")  # Facebook
    hashtags = models.TextField(blank=True, null=True)

    #Adicionales (no están en el formulario)
    campaign_id = models.CharField(max_length=255, null=True, blank=True, default="")
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre
    

class AdSet(models.Model):
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
    daily_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    billing_event = models.CharField(max_length=250, choices=BILLING_EVENTS, blank=True, default="REACH")  # Facebook
    optimization_goal = models.CharField(max_length=250, choices=OPTIMIZATION_GOALS, blank=True, default="REACH")  # Facebook
    status = models.CharField(max_length=255, blank=True)
    
    #Adicionales (no están en el formulario)
    addset_id= models.CharField(blank=True, max_length=100)
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre

    
class Ad(models.Model):
    nombre = models.CharField(max_length=250)
    adset_id= models.CharField(blank=True, max_length=100)
    status = models.CharField(max_length=100)
    creative = models.CharField(max_length=250)
    access_token = models.CharField(max_length=100)

    def __str__(self):
        return self.addset_id
