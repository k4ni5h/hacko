# yomamabot/fb_yomamabot/views.py
import json, requests, random, re
from pprint import pprint
import wikipedia
from django.views import generic
from django.http.response import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from PyDictionary import PyDictionary
from googletrans import Translator
from weather import Weather
from .chat import chat
import json
import math
import datefinder
import datetime
import difflib

PAGE_ACCESS_TOKEN="EAADZB21nljdYBAJaX1S6fvAV2v8XjzZBMAj05CpEgLXnWYJnOLkKaGT7fZBFLskFxfR3QVQwY8xHaBXzAcsy0nZBqAkuE4dxP3o3ikgWBeXF5oBhpGD4qegh7aDDphxOotyZAK6gtKyHnr33kSMoQyLe73Mn8CAgaNzJk872lUwZDZD"


old_bro = '''
{
  "begin":{
    "text": "begin"
   },
  "selection": {
    "text": "Do you want insurance for bike or car",
    "options": ["car","bike"]
  },
  "car_make": {
    "text": "Select the car Make.",
    "fetch_model": "company"
  },
  "car_age": {
    "text": "When did you buy your car.",
    "accepted_answer": {
      "type": "date"
    }
  },
  "car_model": {
    "text": "select model of car",
    "fetch_model": "vehicle"
  },
  "policy": {
    "text": "Have you done any policy before",
    "options": ["yes","no"]
  },
  "expired": {
    "text": "check whether expired or not",
    "options": ["yes","no"]
  },
  "renewal": {
    "text": "do you want to renewal of your policy",
    "options": ["yes","no"]
  },
  "insurance_type": {
    "text": " which type of insurance do you want",
    "options": ["comprehensive", "3rd-party"]
  },
  "adds_on": {
    "text": "do you need any adds on for policy",
    "fetch_model": "add_on"
  },
  "claim": {
    "text": "do you want to claim your insurance",
    "options": ["yes", "no"]
  },
  "checking": {
    "text": "Whether incurance  was before claimed or not",
    "options": ["yes", "no"]
  },
  "claim_details": {
    "text": "how  damage happened to vehicle"
  },
  "claim_checking_type": {
    "text": "check the type of insurance and decide applicable for claim or not"
  },
  "get_info": {
    "text": "display the insurance and user details"
  },
  "appointment": {
    "text": "choose the time for appointment",
    "accepted_answer": {
      "type": "date"
    }
  },
  "location": {
    "text": "Please select your address",
    "accpted_answer": {
      "type": "location"
    }
  },
  "needs": {
    "text": "Select the needs"
  },
  "idv": {
    "text": " enter the idv value",
    "accepted_answer": {
      "type": "int",
      "range": "vehicle"
    }
  }
}
'''

pref_array = ["selection", "car_make", "car_model", "insurance_type", "idv", "adds_on", "location", "number", "time_booking"]

bro = '''
{
  "selection": {
    "text": "Do you want insurance for bike or car",
    "options": ["car","bike"]
  },
  "car_make": {
    "text": "Select the car Make.",
    "fetch_model": "company"
  },
  "car_age": {
    "text": "When did you buy your car.",
    "accepted_answer": {
      "type": "date"
    }
  },
  "car_model": {
    "text": "select model of car",
    "fetch_model": "vehicle"
  },
  "policy": {
    "text": "Have you done any policy before",
    "options": ["yes","no"]
  },
  "expired": {
    "text": "check whether expired or not",
    "options": ["yes","no"]
  },
  "renewal": {
    "text": "do you want to renewal of your policy",
    "options": ["yes","no"]
  },
  "insurance_type": {
    "text": " which type of insurance do you want",
    "options": ["comprehensive", "3rd-party"]
  },
  "adds_on": {
    "text": "do you need any adds on for policy",
    "fetch_model": "add_on"
  },
  "claim": {
    "text": "do you want to claim your insurance",
    "options": ["yes", "no"]
  },
  "checking": {
    "text": "Whether incurance  was before claimed or not",
    "options": ["yes", "no"]
  },
  "claim_details": {
    "text": "how  damage happened to vehicle"
  },
  "claim_checking_type": {
    "text": "check the type of insurance and decide applicable for claim or not"
  },
  "get_info": {
    "text": "display the insurance and user details"
  },
  "appointment": {
    "text": "choose the time for appointment",
    "accepted_answer": {
      "type": "date"
    }
  },
  "location": {
    "text": "Please select your address",
    "accpted_answer": {
      "type": "location"
    }
  },
  "number": {
    "text": "Please provide me your contact number",
    "accpted_answer": {
      "type": "number"
    }
  },
  "idv": {
    "text": " enter the idv value",
    "accepted_answer": {
      "type": "int",
      "range": "vehicle"
    }
  },
  "time_booking": {
    "text": "Please provide your availability",
    "accepted_answer": {
      "type": "date"
    }
  }
}
'''

questions = json.loads(bro)
#pref_array = ['begin', 'selection', 'car_make', 'car_model', 'car_age', 'policy', 'expired', 'renewal', 'insurance_type', 'adds_on', 'claim', 'checking', 'claim_details', 'claim_checking_type', 'get_info', 'appointment', 'location', 'needs', 'idv']

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
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    pprint(incoming_message)
                    try:
                        payload = message['message']['text'] if 'text' in message['message'] else message['message']['attachments']['payload']
                    except:
                        return HttpResponse()
                    post_facebook_message(message['sender']['id'], payload) 
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

    options=['yes', 'no']
    print(recevied_message)
    father(recevied_message, fbid)
    # quick_reply(recevied_message, options, "location", fbid)
    

def quick_reply(question, options, content_type, fbid):

    if content_type != 'location' and content_type != 'user_phone_number':
        opt = [
          {
            "content_type":content_type,
            "title":i,
            "payload":i
          } for i in options
        ]
    else:
        opt = [
          {
            "content_type":content_type
          }
        ]
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+PAGE_ACCESS_TOKEN 
    response_msg = json.dumps({"is_echo":True,"recipient":{"id":fbid}, "message":{"text":question, "quick_replies": opt}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    

def father(response, fbid):
    try:
        user_info = UserInfo.objects.get(fb_id=fbid)
    except:
        user_info = UserInfo.objects.create(fb_id=fbid)
        # user_info.save()

    user_data = json.loads(user_info.user_data)
    
    pprint(user_data)

    if user_data.get("current_question", None) == None:
        user_data["current_question"] = pref_array[0]
        user_info.user_data = json.dumps(user_data)
        user_info.save()

    accept_status = accept_me(response, questions[user_data['current_question']], user_data, user_info, user_data['current_question'])
    if accept_status:
        for key in questions.keys():    
            if key==user_data['current_question']:
                user_data[key]=accept_status
                break
        user_info.user_data = json.dumps(user_data)
        user_info.save()
    if user_data['current_question']=="time_booking":
        send_message(str(user_data), fbid)
    mother(user_data, fbid)






def match(text, m_list, l):
	x = text.split()
	l = len(x) if l > len(x) else l
	a = [" ".join(x[i:i+l]) for i in range(len(x)-l+1)]
	m_ra = [max([difflib.SequenceMatcher(None, l, m).ratio() for l in a]) for m in m_list]
	print(text, m_list, l, m_ra)
	if max(m_ra)>0.5:
		return m_list[m_ra.index(max(m_ra))]
	else:
		return None

def accept_me(response, question, user_data, user_info, current_question):

    pprint(question)
    date_detected = [i for i in datefinder.find_dates(response)][0].strftime("%Y-%m-%d %H:%M") if [i for i in datefinder.find_dates(response)] else False
    companies = list(i.name for i in Company.objects.all())
    flag = False
    if len(companies)>0 and 'car_make' not in user_data:
        car_company_detected = match(response, companies, 2)
        if car_company_detected:
            flag = True
            user_data['car_make'] = car_company_detected
    car_models = list(i.model_code for i in Vehicle.objects.filter(company__name=user_data.get('car_make', "unknown")))
    if len(car_models)>0 and 'car_model' not in user_data:
        car_model_detected = match(response, car_models, 1)
        if car_model_detected:
            user_data['car_model'] = car_model_detected
    # add_on_detected = match(response, list(i.model_code for i in Vehicle.objects.filter(company__name=user_data['car_make'])), 1)
    entity_keys = ["car_age", "car_make", "car_model"]
    if date_detected and current_question=='time_booking':
        return date_detected
    if date_detected:
        user_data['car_age'] = date_detected
    if 'options' in question:
        option_detected = match(response, question['options'], 1)
        if option_detected:
            user_data[current_question] = option_detected
    
    user_info.user_data = json.dumps(user_data)
    
    user_info.save()
    if flag:
        return {}
    if 'options' in question:
        return match(response, question['options'], 1)
    elif 'fetch_model' in question:
        # if question['fetch_model']=='company':
        #     return match(response, list(i.name for i in Company.objects.all()), 2)
        # elif question['fetch_model']=='vehicle':
        #     return match(response, list(i.model_code for i in Vehicle.objects.filter(company__name=user_data['car_make'])), 1)
        if question['fetch_model']=='add_on':
            return match(response, list(i.name for i in Addons.objects.all()), 1)
    elif 'accepted_answer' in question:
        if question['accepted_answer']['type']=='location':
            if 'coordinates' in response:
                return response['coordinates']
        elif question['accepted_answer']['type']=='number':
            return response
        # elif question['accepted_answer']['type']=='date':
        #     return [i for i in datefinder.find_dates(response)][0].strftime("%Y-%m-%d %H:%M") if [i for i in datefinder.find_dates(response)] else False
        elif question['accepted_answer']['type']=='int':
            price = Vehicle.objects.get(company__name=user_data.get('car_make'), model_code=user_data.get('car_model')).vehicle_price
            response_price = re.search('\d+\S+', response).group()
            price_check = re.search('\d+', response_price).group()
            print(price_check)
            if int(price_check)>price*3/5 and int(price_check)<price:
                return response_price
            else:
                False
    return response

def mother(user_data, fbid):
    t_rex = pref_array.index(user_data["current_question"])
    flag=False
    for i in range(t_rex, len(pref_array)):
        if pref_array[i] in user_data:
            flag=True
            continue
        if flag:
            user_data['current_question'] = pref_array[i]
            try:
                user_info = UserInfo.objects.get(fb_id=fbid)
            except:
                user_info = UserInfo.objects.create(fb_id=fbid)
                user_info.save()
            user_info.user_data = json.dumps(user_data)
            user_info.save()
        return ask(questions[pref_array[i]], user_data, pref_array[i], flag, fbid)

def ask(question, user_data, question_key, flag, fbid):

    options = []
    content_type = None
    pre_text = ""
    if not flag:
        pre_text = "I didn't get what you said. Let's try again. "
    additional_text=""
    if question_key in user_data:
        options.append(user_data[question_key])
    if 'options' in question:
        content_type = "text"
        options.extend(question['options'])
    elif 'fetch_model' in question:
        content_type = "text"
        if question['fetch_model']=='company':
            options.extend(list(i.name for i in Company.objects.all())[:5])
        elif question['fetch_model']=='vehicle':
            options.extend(list(i.model_code for i in Vehicle.objects.filter(company__name=user_data['car_make']))[:5])
        elif question['fetch_model']=='add_on':
            options.extend(list(i.name for i in Addons.objects.all())[:5])
    elif 'accepted_answer' in question:
        if question['accepted_answer']['type']=='location':
            content_type = "location"
            options.append("location")
        if question['accepted_answer']['type']=='number':
            content_type = "user_phone_number"
            options.append("Phone number")
        elif question['accepted_answer']['type']=='int':
            price = Vehicle.objects.get(company__name=user_data['car_make'], model_code=user_data['car_model']).vehicle_price
            additional_text = "Ranges from:" + str(price*3/5) + "-" + str(price)
            
    options = list(set(options))
    if options:
        quick_reply(pre_text + question['text'] + additional_text, options, content_type, fbid)
    else:
        send_message(pre_text + question['text'] + additional_text, fbid)

def send_message(sent_message, fbid):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+PAGE_ACCESS_TOKEN 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":sent_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())
    return