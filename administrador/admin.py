from django.contrib import admin
from .models import Campaign, AdSet, Ad, Creative

# Register your models here.
admin.site.register(Campaign)
admin.site.register(AdSet)
admin.site.register(Ad)
admin.site.register(Creative)
