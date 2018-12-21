from flask import Flask, request, render_template
import requests
import time
import json
import os
from bs4 import BeautifulSoup as bs

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_URL = 'https://api.hphk.io/telegram'
CAFE_LIST = {
    '전체' : -1,
    '부천점' : 15,
    '안양점' : 13,
    '대구동성로2호점' : 14,
    '대구동성로점' : 9,
    '궁동직영점' : 1,
    '은행직영점' : 2,
    '부산서면점' : 19,
    '홍대상수점' : 20,
    '강남점' : 16,
    '건대점' : 10,
    '홍대점' : 11,
    '신촌점' : 6,
    '잠실점' : 21,
    '부평점' : 17,
    '익산점' : 12,
    '전주고사점' : 8,
    '천안신부점' : 18,
    '천안점' : 3,
    '천안두정점' : 7,
    '청주점' : 4
}
@app.route('/{}'.format(os.getenv('TELEGRAM_TOKEN')), methods=['POST'])
def telegram() :
    # 텔레그램으로부터 요청이 들어 올 경우, 해당 요청을 처리하는 코드
    #print(request.get_json()["message"]["from"]["id"])
    #print(request.get_json()["message"]["text"])
    response = request.get_json()
    
    """
    {'update_id': 693359414, 'message': {'message_id': 22, 'from': {'id': 748290634, 
    'is_bot': False, 'first_name': 'Jungjung', 'language_code': 'ko'}, 'chat': {'id': 748290634, 
    'first_name': 'Jungjung', 'type': 'private'}, 'date': 1545292109, 'text': '하이하이'}}
    """
    chat_id = response["message"]["from"]["id"]
    #msg = response["message"]["text"]
    txt = response["message"]["text"]

    if(txt == '안녕'):
        msg = "존댓말."
        
    elif(txt == '안녕하세요') :
        msg = "넹"
        
    elif(txt == '환율') :
        url = 'http://info.finance.naver.com/marketindex/exchangeList.nhn'
        response = requests.get(url).text
        soup = bs(response, 'html.parser')
        soup = soup.find_all("td", {"class":{"tit", "sale"}})
        
        exchanges={}
        for i in range(88):
            if(i == 0 or i % 2 == 0):
                exchanges['국가'] = soup[i].text 
            elif(i % 2 == 1) :
                exchanges['환율'] = soup[i].text
        #print(exchanges)
        #print(exchanges[0])
        #print(exchanges[1]["cost"])

        for i in range(len(exchanges)):
            msg += ', '.join("{} = {}".format(key, val) for (key, val) in exchanges.items())
            
    elif(txt.startswith('마스터키')) :
        cafe_name = txt.split(' ')[1]
        
        cd = CAFE_LIST[cafe_name]
        
        if(cd > 0):
            data = master_key_info(cd)
        else :
            data = master_key_list()
        msg = []
        for d in data:
            msg.append('\n'.join(d.values()))
        msg = '\n'.join(msg)

    else:
        msg = '등록되지 않은 메세지입니다.'
    
    
        
    url = 'https://api.hphk.io/telegram/bot{}/sendMessage'.format(TELEGRAM_TOKEN)

    
    requests.get(url, params = {"chat_id" : chat_id, "text" : msg})
    

    return '', 200
    
    
@app.route('/set_webhook')    # alert창 띄우기 
def set_webhook():
    url = TELEGRAM_URL + '/bot' + TELEGRAM_TOKEN + '/setWebhook'
    params = {
        'url' : 'https://sspy-week2-juneun.c9users.io/{}'.format(TELEGRAM_TOKEN)
    }
    response = requests.get(url, params = params).text
    return response
    
    
    
def master_key_info(cd):
    url = 'http://www.master-key.co.kr/booking/booking_list_new'
    params = {
        'date' : '2018-12-22',
        'store' : cd,
        'room' : ''
        
    }
    response = requests.post(url, params).text
    document= bs(response, 'html.parser')
    ul = document.select('.reserve')
    lis = document.select('.reserve .escape_view')
    
    theme_list = []
    for li in lis:
        title = li.select('p')[0].text
        info = ''
        for col in li.select('.col'):
            info = info + '{} - {}\n'.format(col.select_one('.time').text, col.select_one('.state').text)
        
        theme = {
            'title' : title,
            'info' : info
        }
        
        theme_list.append(theme)
        
    return theme_list


def master_key_list():
    url = 'http://www.master-key.co.kr/home/office'
    
    response = requests.get(url).text
    
    document = bs(response, 'html.parser')
    
    # class = .class이름  /  id = #id이름
    ul = document.select('.escape_list')
    
    lis = document.select('.escape_list .escape_view')
    
    CAFE_LIST = []
    for li in lis :
        #print(li.select_one('p').text)
        #print(li.select('dd'))
        #print(li.select_one('a')["href"])
        
        # python how to eliminate string from string
        title = li.select_one('p').text
        if(title.endswith('NEW')) :
            title = title[:-3]
            
        address = li.select('dd')[0].text
        tel = li.select('dd')[1].text
            
        link = 'http://www.master-key.co.kr' + li.select_one('a')["href"]    
        
        cafe = {
            'title' : title,
            'tel' : tel,
            'address' : address,
            'link' : link
        }
        CAFE_LIST.append(cafe)
    
    # print(CAFE_LIST)
    return CAFE_LIST

