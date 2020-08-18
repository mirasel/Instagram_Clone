from django.contrib.auth.views import PasswordResetView,PasswordResetCompleteView,PasswordResetConfirmView
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import auth
from .models import profile

def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username_mail']
            password = request.POST['password']
            try:
                User.objects.get(username=username)
                user = auth.authenticate(username=username,password=password)
                print("usersite")
                if user is not None:
                    auth.login(request,user)
                    return redirect('instagram:feed')
                else:
                    return render(request,'accounts/login.html',{'error':'The password was incorrect. Please double-check your password.'})
            except User.DoesNotExist:
                try:
                    User.objects.get(email=username.lower())
                    username = User.objects.get(email=username.lower()).username
                    user = auth.authenticate(username=username,password=password)
                    print("emailsite")
                    if user is not None:
                        auth.login(request,user)
                        return redirect('instagram:feed')
                    else:
                        return render(request,'accounts/login.html',{'error':'The password was incorrect. Please double-check your password.'})
                except User.DoesNotExist:
                    return render(request,'accounts/login.html',{'error':"The username or email you entered doesn't belong to an account. Please check your username or email and try again."})
        else:
            return render(request,'accounts/login.html',{})
    else:
        return redirect('instagram:feed')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['fullname']
            password = request.POST['password']
            try:
                User.objects.get(username=username)
                return render(request,'accounts/signup.html',{'error':'Username has already taken!',
                                    'input':{'username':username,'password':password,'email':email,'fullname':first_name}})
            except User.DoesNotExist:
                try:
                    User.objects.get(email=email)
                    return render(request,'accounts/signup.html',{'error':'Email has already taken!',
                                        'input':{'username':username,'password':password,'email':email,'fullname':first_name}})
                except User.DoesNotExist:
                    user = User.objects.create_user(username=username,email=email,first_name=first_name,password=password)
                    profile.objects.create(user=user)
                    auth.login(request,user)
                    return redirect('instagram:feed')
        else:
            return render(request,'accounts/signup.html',{})
    else:
        return redirect('instagram:feed')

def logout(request):
    if request.method=='GET':
        auth.logout(request)
        return redirect('accounts:login')

def edit(request):
    u = User.objects.get(username=request.user)
    p = profile.objects.get(user=request.user)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        name = request.POST['name']
        bio = request.POST['bio']
        gender = request.POST['gender']
        u.first_name = name
        p.bio = bio
        p.gender = gender
        u.save()
        p.save()
        if u.email != email:
            try:
                User.objects.get(email=email)
                print("user - ",type(u.email),"post - ",type(email))
                return render(request,'accounts/edit.html',{'u':u,'p':p,'error':'Another account is using '+str(email)})
            except User.DoesNotExist:
                u.email=email
                if u.username != username:
                    try:
                        User.objects.get(username=username)
                        u.save()
                        return render(request,'accounts/edit.html',{'u':u,'p':p,'error':'The Username is already taken! Please try another.'})
                    except User.DoesNotExist:
                        u.username = username
                        u.save()
        else:
            if u.username != username:
                try:
                    User.objects.get(username=username)
                    return render(request,'accounts/edit.html',{'u':u,'p':p,'error':'The Username is already taken! Please try another.'})
                except User.DoesNotExist:
                    u.username = username
                    u.save()
        return redirect('accounts:edit')
    else:
        return render(request,'accounts/edit.html',{'u':u,'p':p})

def change_pro_pic(request):
    u = profile.objects.get(user=request.user)
    if request.is_ajax():
        if request.method == 'POST': 
            action = request.POST.get('action')    
            if action =="default_change":
                u.profile_pic = request.FILES['imgfile']
                u.save()
            else:
                u.profile_pic.delete()
                u.profile_pic = request.FILES['imgfile']
                u.save()
        else:
            action = request.GET.get('action')
            if action =='remove':   
                u.profile_pic.delete()
                u.profile_pic = 'defaultPic/default_profile_pic.jpg'
                u.save()
        return JsonResponse({'url':u.profile_pic.url,'action':action})

def change_password(request):
    u = User.objects.get(username=request.user)
    p = profile.objects.get(user=request.user)
    form = PasswordChangeForm(user=request.user,data=request.POST or None)
    if form.is_valid():
        form.save()
        auth.update_session_auth_hash(request, form.user)
    u = User.objects.get(username=form.user)
    p = profile.objects.get(user=form.user)
    return render(request, 'accounts/edit.html', {'form': form,'u':u,'p':p})

class passwordreset(PasswordResetView):
    template_name='accounts/passwordreset.html'
    email_template_name='accounts/passwordresetemail.html'
    subject_template_name='accounts/passwordresetsubject.txt'
    success_url=reverse_lazy('accounts:password_reset_done')
    extra_context={'done':'reset'}
    
class passwordresetdone(PasswordResetCompleteView):
    template_name='accounts/passwordreset.html'
    extra_context={'done':'email'}

class passwordresetconfirm(PasswordResetConfirmView):
    template_name='accounts/passwordreset.html'
    success_url=reverse_lazy('accounts:password_reset_complete')
    extra_context={'done':'resetform'}

class passwordresetcomplete(PasswordResetCompleteView):
    template_name='accounts/passwordreset.html'
    extra_context={'done':'complete'}