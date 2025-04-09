from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ad, EstadoAd
from django.apps import AppConfig

@receiver(post_save, sender=Ad)
def crear_estado_ad(sender, instance, created, **kwargs):
    if created:
        EstadoAd.objects.create(ad=instance)

class AdministradorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'administrador'

    def ready(self):
        import administrador.signals
