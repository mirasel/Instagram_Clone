from django.urls import path,reverse_lazy,include
from . import views

app_name='accounts'

urlpatterns = [
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('edit',views.edit,name='edit'),
    path('pp_<str:action>',views.change_pro_pic,name='cng_pp'),
    path('password_change',views.change_password,name='password_change'),
    path('password_reset/', views.passwordreset.as_view(), name='password_reset'),
    path('password_reset/done/', views.passwordresetdone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.passwordresetconfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.passwordresetcomplete.as_view(), name='password_reset_complete'),
]