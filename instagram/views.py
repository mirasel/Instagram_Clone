from django.shortcuts import render,redirect
from accounts.models import profile
from django.contrib.auth.models import User
from django.db.models import Q

def get_profile_details(user):
    try:
        p = profile.objects.get(user=user)
        return p
    except profile.DoesNotExist:
        p = profile(user=user)
        p.save()
        return p

def get_nav_propic(request):
    try:
        navpropic = profile.objects.get(user=request.user)
        return navpropic.profile_pic
    except profile.DoesNotExist:
        navpropic=get_profile_details(request)
        return navpropic.profile_pic
def feed(request):
    if request.user.is_authenticated:
        u = User.objects.all().exclude(Q(username=request.user)|Q(is_superuser=1))
        return render(request,'instagram/feed.html',{'profile':get_profile_details(request.user),
                                            'u':u})
    else:
        return redirect('accounts:login')

def get_profile(request,name):
    try:
        u = User.objects.get(username=name)
        return render(request,'instagram/profile.html',{'user_details':u,'profile':get_profile_details(u),'navpropic':get_nav_propic(request)})
    except User.DoesNotExist:
        return redirect('accounts:login')

    