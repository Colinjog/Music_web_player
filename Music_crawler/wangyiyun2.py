import requests


response = requests.request('get',url='https://music.163.com/')
print(response.content.decode('utf-8'))