from django.db import models
from datetime import date

class Campaign(models.Model):
    REDES_SOCIALES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
    ]
    
    OBJECTIVES = [
        ('conversiones', 'Conversiones'),
        ('interacciones', 'Interacción'),
        ('alcance', 'Alcance'),

    ]

    nombre = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    red_social = models.CharField(max_length=20, choices=REDES_SOCIALES, default='facebook')
    formato = models.CharField(max_length=255, blank=True, null=True)
    objective = models.CharField(max_length=250, choices=OBJECTIVES, blank=True, default="Brand Awareness")  # Facebook
    hashtags = models.TextField(blank=True, null=True)

    #Adicionales (no están en el formulario)
    campaign_id = models.CharField(max_length=255, null=True, blank=True, default="")
    created_at = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre
    

'''
class AddSet(models.Model):
    addset_id= models.CharField(blank=True, max_length=100, unique=True)
    campaign_id = models.CharField(max_length=250)
    daily_budjet = models.IntegerField()
    status = models.CharField(max_length=100)
    acces_token = models.CharField(max_length=100)

    def __str__(self):
        return self.addset_id
    
class Add(models.Model):
    name = models.CharField(max_length=250)
    addset_id= models.CharField(blank=True, max_length=100)
    status = models.CharField(max_length=100)
    creative = models.CharField(max_length=250)
    acces_token = models.CharField(max_length=100)

    def __str__(self):
        return self.addset_id
'''