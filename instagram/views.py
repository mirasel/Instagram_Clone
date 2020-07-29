from django.shortcuts import render,redirect
from accounts.models import profile
from django.contrib.auth.models import User

def get_profile_details(user):
    try:
        p = profile.objects.get(user=user)
        return p
    except profile.DoesNotExist:
        p = profile(user=user)
        p.save()
        return p
def feed(request):
    if request.user.is_authenticated:
        return render(request,'instagram/feed.html',{'profile':get_profile_details(request.user)})
    else:
        return redirect('accounts:login')

def get_profile(request,name):
    try:
        u = User.objects.get(username=name)
        return render(request,'instagram/profile.html',{'user_details':u,'profile':get_profile_details(u)})
    except User.DoesNotExist:
        return redirect('instagram:feed')

    