from django.contrib import admin
from .models import Campaign, AdSet, Ad, Creative, Vacante

# Register your models here.
admin.site.register(Campaign)
admin.site.register(AdSet)
admin.site.register(Ad)
admin.site.register(Creative)
admin.site.register(Vacante)

