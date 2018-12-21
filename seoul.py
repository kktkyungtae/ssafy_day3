import requests
import json

url = "http://www.seoul-escape.com/reservation/change_date/"
params = {
    'current_data' : '2018/12/21'
}

response = response.get(url, params = params).text
document = json.loads(response)

print(document["gameRoomList"])
for book in document["bookList"]