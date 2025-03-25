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
    path('campaña/', adminViews.campaña, name='campaña'),
    path('crear_campaña/', adminViews.crear_campaña, name='crear_campaña'),
    path('campañas_creadas/', adminViews.campañas_creadas, name='campañas_creadas'),
    path('ad_set/', adminViews.ad_set, name='ad_set'),
    path('ad/', adminViews.ad, name='ad'),

]

# Configure Admin Titles
admin.site.site_header = "Página administradora de ADAS"
admin.site.site_title = "Titulo de la página administradora"
admin.site.index_title = "Bienvenido al area de administración..."
