from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import PlayedMusic, Account
# Create your views here.


def sign_in(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username+"\n"+password)
        temp = Account.objects.filter(username=username,password=password)

        if temp:
            return HttpResponseRedirect(reverse('home'))
        else:
            error_message = "账户不存在或密码错误"
            return render(request,'login/signin.html', {'error_message':error_message})
    else:
        return render(request,'login/signin.html')

def sign_up(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        print("username:",username)
        print("password:",password)

        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request,'login/register.html')



