from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

def index(request):
    if request.COOKIES.get('username'):
        print(request.COOKIES)
        context = {'music_list': [
            {'music_title': "海阔天空", 'pic_src': 'http://p1.music.126.net/QHw-RuMwfQkmgtiyRpGs0Q==/102254581395219.jpg',
             'music_src': 'http://m10.music.126.net/20181104232354/f95ec5e6b913376846c8db9c3cf48e60/ymusic/c588/bb36/c035/3cf45c286508297bec4135084556cf05.mp3',
             "time": 200, 'author': "Beyond"}, ]}
        return render(request, 'MainView/index.html',context=context)
    else:
        return HttpResponseRedirect(reverse('login:sign_in'))


def default_index(request):
    return render(request,'MainView/index2.html')


def text(request):
    return render(request, 'MainView/test.html')

def search(request):

    if request.method == "POST":
        pass

