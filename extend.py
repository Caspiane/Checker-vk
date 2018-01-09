import requests
import json
import shutil
import os

class loli:
	def url_check(self, login, password, captcha_sid = '', captcha_key = ''):
		headers =  {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
		}
		r = requests.get('https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username=' + login + '&password=' + password + '&captcha_sid=' + captcha_sid + '&captcha_key='+captcha_key, headers=headers)
		data = json.loads(r.text)
		return data

	def save_image(self, img):
		pathid = img.split('=')
		idstr = pathid[1]
		path = "temp/" + pathid[1] + ".jpg"
		r = requests.get(img, stream=True)
		if r.status_code == 200:
			with open(path, 'wb') as f:
				r.raw.decode_content = True
				shutil.copyfileobj(r.raw, f)   
		return idstr

	def clearConsole(self):
		os.system('cls')