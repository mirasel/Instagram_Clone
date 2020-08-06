from django.urls import path
from . import views

app_name='post'

urlpatterns = [
    path('upload_post/',views.upload_post,name='upload_post'),
    path('<slug:slug>/',views.post_details,name='post_details'),
]