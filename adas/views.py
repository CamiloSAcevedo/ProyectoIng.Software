from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
#from .models import AuthorizedPersonnel
#from .models import Alert


# Create your views here.

def home(request):
    return render(request, 'home.html')

"""
def alerts(request):
    alertass=Alert.objects.all()
    return render(request, 'alerts.html', {'alertass':alertass})

def personnel(request):
    personal = AuthorizedPersonnel.objects.all()
    return render(request, 'personnel.html', {'personal': personal})
    
"""
