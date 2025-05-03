from django.urls import path
from . import views

urlpatterns = [
    path('panel/', views.panel, name='panel'),  
    path('estadisticas/', views.estadisticas, name='estadisticas'), 
    path('crear_ads/', views.crear_ads, name='crear_ads'),
    # ---------------------- VER MIS VACANTES ----------------------#
    path('vacantes/', views.mis_vacantes, name='mis_vacantes'),
    path('cargar_excel/', views.cargar_excel, name='cargar_excel'),
    # -------------------------------------------------#

]

