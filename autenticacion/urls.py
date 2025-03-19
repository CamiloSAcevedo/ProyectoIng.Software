from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]