from django.conf.urls import include, url
from .views import MeraBot
urlpatterns = [
                  url(r'^MeraBotHaiBC/?$', MeraBot.as_view()) 
               ]