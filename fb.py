import requests
import time
from threading import Thread
import random 
from pystyle import Colors as color
from rgbprint import gradient_print
import sys
import os
from urllib.parse import urlparse, parse_qs
def get_facebook_id(url):
	parsed_url = urlparse(url)
	if 'query' in parsed_url._asdict():
		query_parameters = parse_qs(parsed_url.query)
		if 'story_fbid' in query_parameters:
			return query_parameters['story_fbid'][0]
	path_parts = parsed_url.path.split("/")
	if len(path_parts) > 3:
		return path_parts[3]
	else:
		return url
def banner():
	bn='''
 _____  _____    _____  _____  _____    ____   _____  _____  _____ 
|   __|| __  |  |     ||     ||     |  |    \ |  |  ||     ||  _  |
|   __|| __ -|  |   --||  |  || | | |  |  |  ||  |  || | | ||   __|
|__|   |_____|  |_____||_____||_|_|_|  |____/ |_____||_|_|_||__| 

[#] Code By Issam Iso 
[#] Facebook: fb.com/fsociety.cyber
	'''
	gradient_print(bn,start_color="blue",end_color='red')
def login(username,password):
	api = 'https://b-api.facebook.com/method/auth.login'
	data = {
	    'access_token': '350685531728%7C62f8ce9f74b12f84c123cc23437a4a32',
	    'format': 'JSON',
	    'sdk_version': '2',
	    'email': username,
	    'locale': 'en_US',
	    'password': password,
	    'sdk': 'ios',
	    'generate_session_cookies': '1',
	    'sig': '3f555f99fb61fcd7aa0c44f58f522ef6',
	}
	api_url = api + '?' + '&'.join([f'{key}={value}' for key, value in data.items()])
	response = requests.get(api_url)
	result = response.json()
	if 'access_token' in result:
		return result['access_token']
	if 'error_msg' in result:
		print(color.red+"[!] error_msg : "+result['error_msg']+color.white)
		sys.exit()

def connent(comment,post_id,token):
	url = f'https://graph.facebook.com/{post_id}/comments'
	params = {
		'access_token': token,
		'message': comment
	}
	response = requests.post(url, params=params)
	if response.status_code == 200:
	    print(color.green+"[+] Comment posted successfully.")
	else:
	    print(color.red+f"[-] Failed to post comment. Status code: {response.status_code}")
def Supper():
	banner()
	token=False
	if os.path.exists('token.conf'):
		with open('token.conf' , 'r') as f:
			tokens=f.read().strip()
			if len(tokens) == 0:
				pass 
			else:
				tk=input(color.blue+"[#] "+color.white+"continue with the saved token (token.conf) [Y/n]: ").strip()
				if tk == 'n':
					pass 
				else:
					token=tokens 
	if not token:
		print(color.yellow+'[1]'+color.green+' Start With Token ')
		print(color.yellow+'[2]'+color.green+' Obtain the account Token  ')
		opt=input(color.red+'[*]'+color.yellow+' Select Option: '+color.white).strip()
		if opt == '1':
			token=input(color.red+'[*]'+color.yellow+' Token: '+color.white).strip()
		if opt == '2':
			token=login(
				username=input(color.red+'[*]'+color.yellow+' Username/Email: '+color.white).strip(),
				password=input(color.red+'[*]'+color.yellow+' Password: '+color.white).strip()
			)
			print(color.blue+"[#] "+color.white+"saved Token : token.conf")
			
	if not token:
		sys.exit(color.red+"[*] token not selected")
	with open('token.conf','w') as f:
		f.write(token)
	
	#print(color.green+"[+] "+color.yellow+'Token: '+color.white+token)
	post_url=input(color.yellow+'[&] Enter url post: ').strip()
	post_id=get_facebook_id(post_url)
	print(color.blue+"[+] post id: "+color.white+post_id)
	comment=input(color.yellow+'[&] Enter your comment: ').strip()
	num=int(input(color.yellow+'[&] Enter your number comment: '))
	if not post_url or not comment:
		sys.exit()
	for i in range(num):
		try:
			connent(comment,post_id,token)
		except Exception as e:
			print(color.red+"[-] "+str(e))

			continue 
if __name__ == "__main__":
	try:
		Supper()
	except KeyboardInterrupt:
		sys.exit()
	except Exception as e:
		sys.exit(color.red+"[-] "+str(e))

	
