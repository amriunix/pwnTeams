from pwnTeams.pwndb import pwndb
# from pwnTeams.foo import bar
from bs4 import BeautifulSoup
from flask import Flask, request, send_from_directory
import pymsteams
import thread
import hashlib
import hmac
import base64
import json

app = Flask(__name__)

# The verification key for the Outgoing Webhook on Microsoft Teams
sharedSecret = ''
# The URL for Incoming Webhook on Microsoft Teams
Webhook = ''
botMessage = pymsteams.connectorcard(Webhook)

def help():
	msg =' ## OSINT </br>\
		   `/pwndb` : Check the email in breaches lists. (eg. /pwndb email@example.com) </br>\
		   `/foo`: bar </br>'
	return msg

functions = {
        "/help": help,
        "/pwndb": pwndb
		# "foo": bar
}

# Setting the Incoming Webhooks
def bot_answer(cmd, arg):
	msg = functions[cmd](arg)
	# Add text to the message.
	botMessage.text(msg)
	# send the message.
	botMessage.send()

def Auth(secret, message, auth): 
	msgHash = "HMAC " + base64.b64encode(hmac.new(base64.b64decode(secret), message, digestmod=hashlib.sha256).digest())
	return (auth == msgHash)

def parse_args(args):
	if len(args) > 1:
		cmd = args[1].lower()
		if cmd == '/help':
			return functions[cmd]()
		elif (len(args) > 2):
			arg = args[2:]
			if cmd in ['/pwndb']: # ['func1','func2','foo','bar]
				try:
					thread.start_new_thread( bot_answer, (cmd, arg, ) )
					msg = 'The task has been scheduled, waiting for the answer!'
				except:
					msg = 'Error: unable to start thread'
			else:
				msg = 'Comand not found, try `/help` for more information!'
		else:
			msg = 'Comand not found, try `/help` for more information!'
	else:
		msg = 'Error while parsing the command, try `/help` for more information!'
	return msg

@app.route('/', methods=['GET','POST'])
def index():
	# To make sure that we received all the data as it is !
	request.implicit_sequence_conversion = False
	auth = request.headers['authorization']
	data = request.get_json()
	message = request.get_data()
	html = data['text']
	soup = BeautifulSoup(html, features="html.parser")
	text = soup.get_text()
	args = text.split()
	results = {}
	results['type'] = 'message'
	if Auth(sharedSecret, message, auth):
		results['text'] = parse_args(args)
	else:
		results['text'] = 'Error: message sender cannot be authenticated.'
	return results, 200

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)

