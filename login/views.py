from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import PlayedMusic, Account
import datetime
# Create your views here.


def sign_in(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username+"\n"+password)
        temp = Account.objects.filter(username=username,password=password)

        if temp:
            res = HttpResponseRedirect(reverse('home'))
            res.set_cookie('username',username,expires=(datetime.datetime.now()+datetime.timedelta(hours=2)))

            return res
        else:
            error_message = "账户不存在或密码错误"
            return render(request,'login/signin.html', {'error_message': error_message})
    else:
        return render(request,'login/signin.html')


def sign_up(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        print("username:",username)
        print("password:",password)
        print("password2:",password2)
        temp = Account.objects.filter(username=username)
        context = {}
        if temp:
            context = {'error_message':"用户名已存在，请重新输入"}
            return render(request,'login/register.html', context=context)
        if password != password2:
            context['error_message'] = "两次输入的密码不同"
            return render(request,'login/register.html', context=context)
        account = Account(username=username, password=password)
        account.save()
        context={'username':username}
        res = HttpResponseRedirect(reverse('home'),context=context)
        res.set_cookie('username',username,expires=(datetime.datetime.now()+datetime.timedelta(hours=2)))

        return res
    else:
        return render(request,'login/register.html')



