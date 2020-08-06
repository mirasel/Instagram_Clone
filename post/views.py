from django.shortcuts import render,redirect
from instagram.views import get_nav_propic,get_profile_details
from .models import UserPost


def upload_post(request):
    if request.method == 'POST':
        image = request.FILES['post_img']
        caption = request.POST['caption']
        uploader = request.user
        UserPost.objects.create(uploader=uploader,image=image,caption=caption)
        return redirect('instagram:feed')
    else:
        context = {
            'propic' : get_nav_propic(request.user)
        }
        return render(request,'post/upload_post.html',context)

def post_details(request,slug):
    post = UserPost.objects.get(slug=slug)
    context = {
        'propic'    : get_nav_propic(request.user),
        'post'      : post,
        'uploader'  : get_profile_details(post.uploader),
    }
    return render(request,'post/post_details.html',context)
