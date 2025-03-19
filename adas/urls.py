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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('administrador/', include('administrador.urls')),
    path('autenticacion/', include('autenticacion.urls')),
    path('autenticacion/', include('django.contrib.auth.urls')),

]

# Configure Admin Titles
admin.site.site_header = "Página administradora de ADAS"
admin.site.site_title = "Titulo de la página administradora"
admin.site.index_title = "Bienvenido al area de administración..."
