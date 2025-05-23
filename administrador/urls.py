from django.urls import path
from . import views
from clustering import views as clusteringViews

urlpatterns = [
    path('panel/', views.panel, name='panel'),  
    path('estadisticas/', views.estadisticas, name='estadisticas'), 

    # Post X
    path('crear_post/', views.crear_post, name='crear_post'),
    # Campaña
    path('campaña/', views.campaña, name='campaña'),
    path('crear_campaña/', views.crear_campaña, name='crear_campaña'),
    path('mis_campañas/', views.mis_campañas, name='mis_campañas'),
    # AdSet
    path('obtener_optimization_goals/', views.obtener_optimization_goals, name='obtener_optimization_goals'),
    path('ad_set/', views.ad_set, name='ad_set'),
    path('crear_adset/', views.crear_adset, name='crear_adset'),
    path('mis_adsets/', views.mis_adsets, name='mis_adsets'),
    # Ad
    path('ad/', views.ad, name='ad'),
    path('crear_ad/', views.crear_ad, name='crear_ad'),
    path('mis_ads/', views.mis_ads, name='mis_ads'),
    #Creative
    path('crear_creative/', views.crear_creative, name='crear_creative'),
    path('mis_creatives/', views.mis_creatives, name='mis_creatives'),
    # Administración de contenido (ads y posts)
    path("revisar/<str:tipo>/pendientes/", views.revisar_contenido_pendiente, name="revisar_contenido_pendiente"),
    path("aprobar/<str:tipo>/<str:objeto_id>/", views.aprobar_contenido, name="actualizar_estado_contenido"),
    path("mis-solicitudes/<str:tipo>/", views.mis_solicitudes_contenido, name="mis_solicitudes_contenido"),

    # Vacantes
    path('vacantes/', views.mis_vacantes, name='vacantes'),
    path('cargar_excel/', views.cargar_excel, name='cargar_excel'),
    # ---------------------- VER MIS VACANTES ----------------------#
    path('vacantes/', views.mis_vacantes, name='mis_vacantes'),
    path('cargar_excel/', views.cargar_excel, name='cargar_excel'),
    # -------------------------------------------------#

    #Clustering
    path('mis_modelos/', clusteringViews.ver_modelos_entrenados, name='mis_modelos'),
    path('entrenar_modelo/', clusteringViews.entrenar_modelo, name='entrenar_modelo'),
    path('mis_clusters/', clusteringViews.ver_clusters, name='mis_clusters'),
    path('clusters/<int:modelo_id>/<int:cluster>/targeting/', clusteringViews.definir_targeting, name='definir_targeting'),
    path('clusters/<int:modelo_id>/<int:cluster>/targeting/generar_ia/', clusteringViews.generar_targeting_ia, name='generar_targeting_ia'),


]

