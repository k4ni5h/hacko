# yomamabot/fb_yomamabot/views.py
import json, requests, random, re
from pprint import pprint
import wikipedia
from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from PyDictionary import PyDictionary
from googletrans import Translator
from weather import Weather
from .chat import chat

import math

PAGE_ACCESS_TOKEN="EAADZB21nljdYBAJaX1S6fvAV2v8XjzZBMAj05CpEgLXnWYJnOLkKaGT7fZBFLskFxfR3QVQwY8xHaBXzAcsy0nZBqAkuE4dxP3o3ikgWBeXF5oBhpGD4qegh7aDDphxOotyZAK6gtKyHnr33kSMoQyLe73Mn8CAgaNzJk872lUwZDZD"

def isevaluable(s):
    try:
        eval(s)
        return True
    except:
        return False

# Train based on the english corpus
weather=Weather()

class MeraBot(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == 'hacko_1.0halla_b0l':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    # The get method is the same as before.. omitted here for brevity
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        pprint(incoming_message)
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    post_facebook_message(message['sender']['id'], message['message']['text']) 
        return HttpResponse()

class Privacy(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('MY PRIVACIES ARE NOTHING')
    # The get method is the same as before.. omitted here for brevity
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        return HttpResponse('MY PRIVACIES ARE NOTHING')


def post_facebook_message(fbid, recevied_message):

    sent_message="hello"

    send_message(fbid, sent_message)
    return


def send_message(fbid, sent_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+PAGE_ACCESS_TOKEN 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":sent_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())
    return