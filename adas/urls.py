"""
URL configuration for adas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from adas import views as adasViews
from administrador import views as adminViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('administrador/', include('administrador.urls')),
    path('autenticacion/', include('autenticacion.urls')),
    path('autenticacion/', include('django.contrib.auth.urls')),
    path('', adasViews.home, name='home'),
    path('panel/', adminViews.panel, name='panel'),
    path('estadisticas/', adminViews.estadisticas, name='estadisticas'),
    # Campaña
    path('campaña/', adminViews.campaña, name='campaña'),
    path('crear_campaña/', adminViews.crear_campaña, name='crear_campaña'),
    path('mis_campañas/', adminViews.mis_campañas, name='mis_campañas'),
    # AdSet
    path('obtener_optimization_goals/', adminViews.obtener_optimization_goals, name='obtener_optimization_goals'),
    path('ad_set/', adminViews.ad_set, name='ad_set'),
    path('crear_adset/', adminViews.crear_adset, name='crear_adset'),
    path('mis_adsets/', adminViews.mis_adsets, name='mis_adsets'),
    # Ad
    path('ad/', adminViews.ad, name='ad'),
    path('crear_ad/', adminViews.crear_ad, name='crear_ad'),
    path('mis_ads/', adminViews.mis_ads, name='mis_ads'),
    #Creative
    #path('creative/', adminViews.creative, name='creative'),
    path('crear_creative/', adminViews.crear_creative, name='crear_creative'),
    path('mis_creatives/', adminViews.mis_creatives, name='mis_creatives'),
    # Administración de ads
    path("ads-pendientes/", adminViews.revisar_ads_pendientes, name="revisar_ads_pendientes"),
    path("ads/<int:ad_id>/actualizar-estado/", adminViews.aprobar_ad, name="actualizar_estado_ad"),
    path("mis-ads/", adminViews.mis_solicitudes_ads, name="mis_solicitudes_ads"),
]

# Configure Admin Titles
admin.site.site_header = "Página administradora de ADAS"
admin.site.site_title = "Titulo de la página administradora"
admin.site.index_title = "Bienvenido al area de administración..."
