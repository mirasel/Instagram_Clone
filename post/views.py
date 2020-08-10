from django.shortcuts import render,redirect
from instagram.views import get_nav_propic,get_profile_details
from .models import UserPost,PostComment,PostLike
from django.http import JsonResponse

def get_post_likes(post):
    likes = PostLike.objects.filter(post=post)
    total_likes = len(likes)
    likers = []
    for l in likes:
        likers.append(get_profile_details(l.liker))
    return {'likers':likers,'total_likes':total_likes}


def get_post_comments(post):
    comments = PostComment.objects.filter(post=post)
    total_comments = len(comments)
    commenter = []
    comment = []
    for c in comments:
        commenter.append(get_profile_details(c.commenter))
        comment.append(c.comment)
    postcomment = zip(commenter,comment)
    return {'post_comment':postcomment,'total_comments':total_comments}


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
    print('I am here in post details')
    post = UserPost.objects.get(slug=slug)
    context = {
        'propic'    : get_nav_propic(request.user),
        'post'      : post,
        'uploader'  : get_profile_details(post.uploader),
        'LIKES'     : get_post_likes(post),
        'COMMENTS'  : get_post_comments(post),
    }
    return render(request,'post/post_details.html',context)

def add_comment(request):
    print('I am here in add comment')
    if request.method == 'POST':
        post_slug = request.POST.get('slug')
        post = UserPost.objects.get(slug=post_slug)
        user = request.user
        comment = request.POST.get('comment')
        PostComment.objects.create(post=post,commenter=user,comment=comment)
        return redirect('post:post_details',slug=post_slug)

    
    
