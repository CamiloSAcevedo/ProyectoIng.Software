from django.urls import path
from . import views

urlpatterns = [
    path('panel/', views.panel, name='panel'),  
    path('estadisticas/', views.estadisticas, name='estadisticas'), 
    
    # Gemini 
    path('creative/generar-message/', views.generar_message_ia, name='generar_message_ia'),
    path('creative/generar-body/', views.generar_body_ia, name='generar_body_ia'),
    path('buscar_vacante/', views.buscar_vacante, name='buscar_vacante'),

    path('set_plataforma/', views.set_plataforma, name='set_plataforma'),

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

    # ---------------------- VER MIS VACANTES ----------------------#
    #path('vacantes/', views.mis_vacantes, name='mis_vacantes'),
    path('cargar_excel/', views.cargar_excel, name='cargar_excel'),

    # ---------------------- POSTS EN TIKTOK ----------------------#
    path('crear_post_tiktok/', views.crear_post_tiktok, name='crear_post_tiktok'),
    path('mis_solicitudes_contenido/post_tiktok/', views.mis_solicitudes_post_tiktok, name='mis_solicitudes_contenido_post_tiktok'),
    path('revisar_contenido_pendiente/post_tiktok/', views.revisar_contenido_pendiente_post_tiktok, name='revisar_contenido_pendiente_post_tiktok'),

    path('tiktok/advertisers/', views.advertiser_tiktok_list, name='advertiser_tiktok_list'),
    path('tiktok/advertisers/create/', views.advertiser_tiktok_create, name='advertiser_tiktok_create'),
    path('tiktok/advertisers/<int:advertiser_id>/campaigns/', views.campaign_tiktok_list, name='campaign_tiktok_list'),
    path('tiktok/advertisers/<int:advertiser_id>/campaigns/create/', views.campaign_tiktok_create, name='campaign_tiktok_create'),
    path('tiktok/campaigns/<int:campaign_id>/adgroups/', views.adgroup_tiktok_list, name='adgroup_tiktok_list'),
    path('tiktok/campaigns/<int:campaign_id>/adgroups/create/', views.adgroup_tiktok_create, name='adgroup_tiktok_create'),
    path('tiktok/adgroups/<int:adgroup_id>/ads/', views.ad_tiktok_list, name='ad_tiktok_list'),
    path('tiktok/adgroups/<int:adgroup_id>/ads/create/', views.ad_tiktok_create, name='ad_tiktok_create'),
    path('tiktok/adgroups/', views.adgroup_tiktok_all, name='adgroup_tiktok_all'),
    path('tiktok/ads/', views.ad_tiktok_all, name='ad_tiktok_all'),
    path('tiktok/adgroups/create/', views.adgroup_tiktok_create_select_campaign, name='adgroup_tiktok_create_select_campaign'),
    path('tiktok/ads/create/', views.ad_tiktok_create_select_adgroup, name='ad_tiktok_create_select_adgroup'),

    # Listar todos los Ads publicados (público)
    path('tiktok/ads/', views.ads_tiktok_publicados, name='ads_tiktok_publicados'),

    # Listar Ads pendientes para revisión (solo admin/staff)
    path('tiktok/ads/pendientes/', views.revisar_ads_tiktok, name='revisar_ads_tiktok'),

    # Aprobar o rechazar un Ad (solo admin/staff)
    path('tiktok/ads/aprobar/<int:ad_id>/', views.aprobar_rechazar_ad_tiktok, name='aprobar_rechazar_ad_tiktok'),

    # Ver mis solicitudes de Ads (usuario)
    path('tiktok/ads/mis-solicitudes/', views.mis_solicitudes_ads_tiktok, name='mis_solicitudes_ads_tiktok'),



    # AUTORELLENO VACANTES A POST X 
    path('obtener-vacante/<int:vacante_id>/', views.obtener_vacante, name='obtener_vacante'),
    


]

