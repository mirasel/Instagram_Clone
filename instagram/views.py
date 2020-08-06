from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import profile
from post.models import UserPost
from django.contrib.auth.models import User
from django.db.models import Q

#--------getting staff from database------------
def get_profile_details(user):
    p = profile.objects.get(user=user)
    return p

def get_nav_propic(user):
    navpropic = profile.objects.get(user=user)
    return navpropic.profile_pic

def get_user_posts(user):
    try:
        posts = UserPost.objects.filter(Q(slug__startswith=user))
        return posts
    except UserPost.DoesNotExist:
        return []

#--------end of getting staff------------

#------feed view------
def feed(request):
    if request.user.is_authenticated:
        user = User.objects.all().exclude(Q(username=request.user)|Q(is_superuser=1))
        context = {
            'propic'   : get_nav_propic(request.user),
            'u'        : user
        }
        return render(request,'instagram/feed.html',context)
    else:
        return redirect('accounts:login')

#Profile view----
def User_profile(request,name):
    u = get_object_or_404(User,username=name)
    context={
        'user_details'  : u,
        'profile'       : get_profile_details(u),
        'propic'     : get_nav_propic(request.user),
        'posts'         : get_user_posts(name)
    }
    return render(request,'instagram/profile.html',context)
