from django.urls import path
from . import views as clusteringViews

urlpatterns = [

    #Clustering
    path('mis_modelos/', clusteringViews.ver_modelos_entrenados, name='mis_modelos'),
    path('entrenar_modelo/', clusteringViews.entrenar_modelo, name='entrenar_modelo'),
    path('mis_clusters/', clusteringViews.ver_clusters, name='mis_clusters'),

]