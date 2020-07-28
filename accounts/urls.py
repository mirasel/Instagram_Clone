from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('edit',views.edit,name='edit'),
    path('pp_<str:action>',views.change_pro_pic,name='cng_pp'),
]