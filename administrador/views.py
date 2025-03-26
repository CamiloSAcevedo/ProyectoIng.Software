import tweepy
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
#from django.contrib.auth.decorators import login_required
#from .models import AuthorizedPersonnel
#from .models import Alert


# Create your views here.
#@login_required esto es de autenticacion
def panel(request):
    return render(request, 'panel.html')

#@login_required
def estadisticas(request):
    return render(request, 'estadisticas.html')

#@login_required
def crear_ads(request):
    return render(request, 'crear_ads.html')


# ---------------------- API DE X ----------------------#
# Configurar autenticación con Tweepy
# Autenticación con la API v2
client = tweepy.Client(
    consumer_key=settings.TWITTER_API_KEY,
    consumer_secret=settings.TWITTER_API_SECRET,
    access_token=settings.TWITTER_ACCESS_TOKEN,
    access_token_secret=settings.TWITTER_ACCESS_SECRET
)

#@login_required
def crear_ads(request):
    if request.method == "POST":
        tweet_text = request.POST.get("tweet")
        if tweet_text:
            try:
                client.create_tweet(text=tweet_text)  # Publica el tweet
                messages.success(request, "¡Tweet publicado correctamente!")
            except Exception as e:
                messages.error(request, f"Error al publicar el tweet: {str(e)}")

        return redirect("crear_ads")  # Redirecciona a la misma página
    
    return render(request, "crear_ads.html")


