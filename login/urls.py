from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'login'
urlpatterns = [path('sign_in/', views.sign_in, name='sign_in'),
               path('sign_up/',views.sign_up,name='sign_up')]

