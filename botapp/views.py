from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
# Create your views here.

from giphy import get_gif


from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt

import requests
import json

def hello(request):

	html="""
	<html><body>
	Hey</body></html>"""
	return HttpResponse(html)


class CommonUrl(generic.View):

	def get(self, request, *args, **kwargs):
		return HttpResponse("Hello")

class Chatbot(generic.View):

	def get(self, request, *args, **kwargs):
		print self.request.GET
		if self.request.GET.get('hub.verify_token') == '123456789':
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self,request,*args,**kwargs)

	"""def post(self,request,*args,**kwargs):
		message=json.loads(self.request.body.encode('utf-8'))
		for entry in message['entry']:
			for msg in entry['messaging']:
				print msg['message']['text']
				reply_to_message(msg['sender']['id'], msg['message']['text'])


		return HttpResponse("None")	"""

	def post(self, request, *args, **kwargs):
		message = json.loads(self.request.body.encode('utf-8'))

		for entry in message['entry']:
			for msg in entry.get('messaging'):
				print msg.get('message')

				if "text" in msg.get('message').keys():
					reply_to_message(msg.get('sender')['id'], msg.get('message')['text'])
				else:
					print "Some Error!!!"

		return HttpResponse("None")	



def reply_to_message(user_id, message):
	access_token = 'EAAUR5KxFUYYBAPWADCTxLHbBWQTKFZAfUzk3RqV6GZCKXHp5MaESZASqPXOh3BJiS9RwpKTaDa62HdRmZBxqVdlWhKPi5xKVlydjDCPQwKlOLKpnk5HIbLRH5qgEB9cr60trijK2XORQiwkHh8W4B6a3HaasJYagEnaZBHK3ZARAZDZD'
	url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token

	resp, attach_link = generate_response(message)
	#send_resp = {"recipient":{"id":user_id}, "message":{"text":resp, "attachment":{"type":"image", "payload":{"url": attach_link}}}}
	send_resp = {"recipient":{"id":user_id}, "message":{"attachment":{"type":"image", "payload":{"url": attach_link}}}}
	response_msg = json.dumps(send_resp)
	status = requests.post(url, headers={"Content-Type": "application/json"},data=response_msg)
	print status.json()

def generate_response(msg):
	if 'search' in msg:
		q = ''.join([ix for ix in msg.split('search', 1)[1]])
	else:
		q = msg
	url_to_send, gif_link = get_gif(q)
	print gif_link
	return url_to_send, gif_link