import json
import os
import time
import config

from extend import loli
from python_rucaptcha import ImageCaptcha
from python_rucaptcha import RuCaptchaControl

# Введите ключ от сервиса RuCaptcha, из своего аккаунта
RUCAPTCHA_KEY = config.RUCAPTCHA_KEY

# Со скольки начинается отсчет
i = 0
# Ошибки каптчи
err = 0
valid = 0
req = loli()

quest = input("""
			    Выберете формат данных: 
				\r\n
				1 - Json формат\r\n
				2 - Обычный формат
	""")

if(quest == 1):
	fileName = 'data_json.txt'
else:
	fileName = 'data_text.txt'

with open(fileName, mode='r', encoding='utf8') as f:
	if(quest == 1):
		read_data = json.loads(f.read())
	else:
		 read_data = f.readlines()
	
	save = open('result.txt', 'a')
	for el in read_data:
		spl = el.split(" ")
		login = spl[0]
		password = spl[1]
		apivk = req.url_check(login, password)
		if('access_token' in apivk):
			save.write(apivk['access_token'] + '\r\n')
			valid += 1
		else:
			print('Error: ' + apivk['error'])
			if(apivk['error'] == 'need_captcha'):
				idstr = req.save_image(apivk['captcha_img'])
				# Ссылка на изображения для расшифровки
				captcha_file = "temp/" + idstr + ".jpg"

				# Возвращается строка-расшифровка капчи
				user_answer = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(captcha_file=captcha_file)
				if user_answer['errorId'] == 0:
					# решение капчи
					# print(user_answer['captchaSolve'])
					# user_answer['taskId']
					apivk1 = req.url_check(login, password, idstr, user_answer['captchaSolve'])
					if('access_token' in apivk1):
						save.write(apivk1['access_token'] + '\r\n')
						valid += 1
					else:
						if(apivk1['error'] == 'need_captcha'):
							err += 1
				elif user_answer['errorId'] == 1:
					# Тело ошибки, если есть
					print(user_answer['taskId'])
					print(user_answer['errorBody'])
					time.sleep(5)
					answer = RuCaptchaControl.RuCaptchaControl(rucaptcha_key = RUCAPTCHA_KEY).additional_methods(action = 'get', id = user_answer['taskId'])
					apivk2 = req.url_check(login, password, idstr, answer['serverAnswer'])
					if('access_token' in apivk2):
						save.write(apivk2['access_token'] + '\r\n')
						valid += 1
					else:
						if(apivk2['error'] == 'need_captcha'):
							err += 1
				os.remove(captcha_file)
		req.clearConsole()
		i += 1
		# Get balance
		answer = RuCaptchaControl.RuCaptchaControl(rucaptcha_key = RUCAPTCHA_KEY).additional_methods(action = 'getbalance')
		print("Проверено: {}/{}".format(i, len(read_data)))
		print("Удачных: {}".format(valid))
		print("Баланс: {} рублей".format(answer['serverAnswer']))
		print("Ошибочные катчи: {}".format(err))
		
		
		# if (i == 10):
		# 	break
	save.close()
print("\r\nУспешно сохранено в {}:\r\n".format(save.name))
input("Нажмите любую клавишу для выхода....")