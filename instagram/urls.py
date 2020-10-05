from django.urls import path
from . import views

app_name = 'instagram'

urlpatterns =[
    path('',views.Feed.as_view(),name='feed'),
    path('<name>/',views.ProfileDetailView.as_view(),name='profile'),
]