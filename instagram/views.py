from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import profile
from post.models import UserPost
from django.contrib.auth.models import User
from django.db.models import Q
from django.views import generic

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
# def feed(request):
#     if request.user.is_authenticated:
#         user = User.objects.all().exclude(Q(username=request.user)|Q(is_superuser=1))
#         context = {
#             'propic'   : get_nav_propic(request.user),
#             'u'        : user
#         }
#         return render(request,'instagram/feed.html',context)
#     else:
#         return redirect('accounts:login')

#Profile view----
# def User_profile(request,name):
#     u = get_object_or_404(User,username=name)
#     context={
#         'user_details'  : u,
#         'profile'       : get_profile_details(u),
#         'propic'        : get_nav_propic(request.user),
#         'posts'         : get_user_posts(name)
#     }
#     return render(request,'instagram/profile.html',context)
class Feed(generic.ListView):
    
    model = UserPost
    template_name = 'instagram/feed.html'
    ordering = '-date_published'
    paginate_by = 7

    def get_queryset(self):
        objects = super(Feed,self).get_queryset()
        # post_uploaders = [i.uploader for i in objects]
        # post_uploaders = list(set(post_uploaders))

        return objects

    def get(self,request,*args,**kwargs):
        if self.request.user.is_authenticated:
            self.extra_context = {
                'propic'        : get_nav_propic(self.request.user),
            }
            return super(Feed,self).get(request,*args,**kwargs)
        else:
            return redirect('accounts:login')

class ProfileDetailView(generic.DetailView):
    template_name = 'instagram/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'name'
    model = User
    
    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        userobj = self.get_object()
        context['profile'] = get_profile_details(userobj)
        context['propic'] = get_nav_propic(self.request.user)
        context['posts'] = get_user_posts(self.kwargs.get('name'))
        return context
    

