from flask import Flask, request
import requests
import json

import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_URL = 'https://api.hphk.io/telegram'

@app.route('/{}'.format(os.getenv('TELEGRAM_TOKEN')), methods=['POST'])
def telegram():
    #텔레그램으로 부터 요청이 들어올 경우, 해당 요청을 처리하는 코드
    req = request.get_json()
    chat_id = req["message"]["from"]["id"]
    if(req["message"]["text"]=="안녕"):
        msg = "첫 만남에는존댓말을 써야죠!"
    elif(req["message"]["text"] == "안녕하세요"):
            msg = "인사 잘하신다 ㅋㅋㅋ"
    url = 'https://api.hphk.io/telegram/bot{}/sendMessage'.format(TELEGRAM_TOKEN)
    requests.get(url, params = {"chat_id" : chat_id, "text" : msg})
    return '', 200

@app.route('/set_webhook')
def set_webhook():
    url = TELEGRAM_URL + '/bot' + TELEGRAM_TOKEN + '/set_webhook'
    params = {
        'url': 'https://ssafy-week2-kktkyungtae.c9users.io/{}'.format(TELEGRAM_TOKEN)
    }
    response = requests.get(url, params = params).text
    return response