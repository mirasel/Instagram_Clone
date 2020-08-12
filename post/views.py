from django.shortcuts import render,redirect,get_object_or_404
from instagram.views import get_nav_propic,get_profile_details
from .models import UserPost,PostComment
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q

def get_post_comments(post):
    comments = PostComment.objects.filter(post=post)
    total_comments = len(comments)
    commenter = []
    comment = []
    for c in comments:
        commenter.append(get_profile_details(c.commenter))
        comment.append(c)
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
    post = get_object_or_404(UserPost,slug=slug)
    context = {
        'propic'    : get_nav_propic(request.user),
        'post'      : post,
        'uploader'  : get_profile_details(post.uploader),
        'LIKES'     : {'likers':post.likes.all(),'total_likes':post.total_likes()},
        'COMMENTS'  : get_post_comments(post),
    }
    return render(request,'post/post_details.html',context)

def add_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = UserPost.objects.get(pk=post_id)
        user = request.user
        comment = request.POST.get('comment')
        post_comment=PostComment.objects.create(post=post,commenter=user,comment=comment)
        if request.is_ajax():
            name = user.username
            propic = get_nav_propic(user)
            data = {
                'name':name,
                'propic':propic.url,
                'comment':comment,
                'id':post_comment.id
            }
            return JsonResponse(data)

def delete_comment(request):
    if request.is_ajax:
        comment_id = request.GET.get('id')
        comment = get_object_or_404(PostComment,pk=comment_id)
        comment.delete()
        return JsonResponse({'id':comment_id})
        
def edit_like(request):
    if request.is_ajax():
        post_id = request.GET.get('id')
        post = get_object_or_404(UserPost,pk=post_id)
        if request.GET.get('event') == 'Like':
            post.likes.add(request.user)
            return JsonResponse({'button':'Unlike'})
        else:
            post.likes.remove(request.user)
            return JsonResponse({'button':'Like'})

    
    
