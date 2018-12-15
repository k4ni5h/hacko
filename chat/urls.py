from django.conf.urls import include, url
from chat.views import MeraBot, Privacy
urlpatterns = [
                  url(r'^MeraBot/?$', MeraBot.as_view()),
                  url(r'^privacy/?$', Privacy.as_view()),
               ]