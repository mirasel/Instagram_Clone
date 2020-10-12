from django.shortcuts import render,redirect,get_object_or_404
from .models import UserPost,PostComment
from accounts.models import profile
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q

def upload_post(request):
    if request.method == 'POST':
        image = request.FILES['post_img']
        caption = request.POST['caption']
        uploader = request.user
        UserPost.objects.create(uploader=uploader,image=image,caption=caption)
        return redirect('instagram:feed')
    else:
        return render(request,'post/upload_post.html',context)

def post_details(request,slug):
    post = get_object_or_404(UserPost,slug=slug)
    context = {'post': post}
    return render(request,'post/post_details.html',context)

def add_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        comment = request.POST.get('comment')
        user = get_object_or_404(profile,user=request.user)
        post = UserPost.objects.get(pk=post_id)
        post_comment=PostComment.objects.create(post=post,commenter=user,comment=comment)
        if request.is_ajax():
            data = {
                'name':post_comment.commenter.user.username,
                'propic':post_comment.commenter.profile_pic.url,
                'comment':post_comment.comment,
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
            response = {'button':'Unlike','total_likes':post.total_likes()}
            if post.total_likes():
                response['last_liker_name'] = post.likes.last().profiles.first().user.username
                response['last_liker_propic'] = post.likes.last().profiles.first().profile_pic.url
            return JsonResponse(response)
        else:
            post.likes.remove(request.user)
            response = {'button':'Like','total_likes':post.total_likes()}
            if post.total_likes():
                response['last_liker_name'] = post.likes.last().profiles.first().user.username
                response['last_liker_propic'] = post.likes.last().profiles.first().profile_pic.url
            return JsonResponse(response)

    
    
