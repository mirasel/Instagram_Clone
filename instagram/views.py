from django.shortcuts import render,redirect
from accounts.models import profile
from django.contrib.auth.models import User

def get_profile_details(request):
    try:
        p = profile.objects.get(user=request.user)
        return p
    except profile.DoesNotExist:
        p = profile(user=request.user)
        p.save()
        return p
def feed(request):
    if request.user.is_authenticated:
        
        return render(request,'instagram/feed.html',{'profile':get_profile_details(request)})
    else:
        return redirect('accounts:login')

def get_profile(request,u_name):
    u = User.objects.get(username=u_name)
    return render(request,'instagram/profile.html',{'user_details':u,'profile':get_profile_details(request)})