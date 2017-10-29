from django.conf.urls import include, url
from chat.views import MeraBot
urlpatterns = [
                  url(r'^MeraBotHaiBC/?$', MeraBot.as_view()) 
               ]