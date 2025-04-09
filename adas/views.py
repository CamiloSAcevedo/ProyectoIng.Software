from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
#from .models import AuthorizedPersonnel
#from .models import Alert


# Create your views here.

def home(request):
    return render(request, 'home.html')

def nosotros(request):
    return render(request, 'nosotros.html',  {'active': 'nosotros'})

def servicios(request):
    return render(request, 'servicios.html', {'active': 'servicios'})

def inicio(request):
    return render(request, 'home.html', {'active': 'inicio'})

"""
def alerts(request):
    alertass=Alert.objects.all()
    return render(request, 'alerts.html', {'alertass':alertass})

def personnel(request):
    personal = AuthorizedPersonnel.objects.all()
    return render(request, 'personnel.html', {'personal': personal})
    
"""
