# yomamabot/fb_yomamabot/views.py
import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from chatterbot import ChatBot
from PyDictionary import PyDictionary
from googletrans import Translator

chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)
trans=Translator()
# Train based on the english corpus
chatbot.train("chatterbot.corpus.english")

class MeraBot(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '2611bombay':
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
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    print('message',message)
                    post_facebook_message(message['sender']['id'], trans.translate(message['message']['text']).text)
        return HttpResponse()

# This function should be outside the BotsView class
def post_facebook_message(fbid, recevied_message):
    line=bot(fbid, str(recevied_message))
    short_message=[line[i:i+640] for i in range(0, len(line), 640)]
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAY95nBokmEBACAsQRp4E9NVsXQgKWdIyrTItZC1qWk4tr0hm0eJvgCBSc6TGJGpYwmitbFxQW3KJY2l1P9cW7nj391OFHlvSvBnHt8XJZAMyAAZAdmEDSoiZBI6mbQqn7XX8n1M9ZA6FLnvBP99xNrozPJZBzjy0zoOghCqZAqXgZDZD'
    for i in range(len(short_message)):
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":short_message[i]}})
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
        print('status',status.json())

def bot(fbid, messages):
    mess=re.sub("[^\w]", " ", messages.lower()).split()
    send=''
    if len(mess)>0:
        if 'hi' in mess or 'hello' in mess or 'hi'==mess[0][0:2]:
            user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
            user_details_params = {'fields':'first_name,last_name,gender', 'access_token':'EAAY95nBokmEBACAsQRp4E9NVsXQgKWdIyrTItZC1qWk4tr0hm0eJvgCBSc6TGJGpYwmitbFxQW3KJY2l1P9cW7nj391OFHlvSvBnHt8XJZAMyAAZAdmEDSoiZBI6mbQqn7XX8n1M9ZA6FLnvBP99xNrozPJZBzjy0zoOghCqZAqXgZDZD'}
            user = requests.get(user_details_url, user_details_params).json()
            print('user', str(user))
            if user['first_name'].lower()=='kanish':
                send = 'yes boss'
            elif user['gender'].lower()=='male':
                send = 'bol BC'
            elif user['gender'].lower()=='female':
                send = 'mujhe ye rishta manjoor hai'
            else:
                send = 'hello '+user['first_name']
        elif 'mean'==mess[-1][0:5] and len(mess)>1:
            for i in range(0, len(mess)-1):
                send+=mess[i]+'\n'
                meaning=PyDictionary(mess[i]).getMeanings()[mess[i]]
                if meaning:
                    for key in meaning:
                        send+=key+' : '+str(meaning[key])+'\n'
                    send+='\n'
                else:
                    send+='Meaning not Found\n'
        elif 'syno'==mess[-1][0:5] and len(mess)>1:
            for i in range(0, len(mess)-1):
                if PyDictionary(mess[i]).getSynonyms()[0]:
                   send+=mess[i]+' : '+str(PyDictionary(mess[i]).getSynonyms()[0][mess[i]])
                else:
                    send+=mess[i]+' : Not Found'
                send+='\n'
        elif 'anto'==mess[-1][0:5] and len(mess)>1:
            for i in range(0, len(mess)-1):
                if PyDictionary(mess[i]).getAntonyms()[0]:
                    send+=mess[i]+' : '+str(PyDictionary(mess[i]).getAntonyms()[0][mess[i]])
                else:
                    send+=mess[i]+' : Not Found'
                send+='\n'
        elif 'trans'==mess[-1][0:5] and len(mess)>1:
            if mess[-2][0:2]=='en' and len(mess)>2:
                send=str(trans.translate(messages.rsplit(' ', 2)[0],dest='en').text)
            else:
                send=str(trans.translate(messages.rsplit(' ', 1)[0],dest='hi').text)
        else:
            send=str(chatbot.get_response(messages))
    else:
        send=messages
    return send