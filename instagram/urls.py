from django.urls import path
from . import views\

app_name = 'instagram'

urlpatterns =[
    path('',views.feed,name='feed'),
    path('<str:u_name>/',views.get_profile,name='profile'),
]