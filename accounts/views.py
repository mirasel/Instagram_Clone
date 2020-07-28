from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import profile

def login(request):
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

def signup(request):
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
                auth.login(request,user)
                return redirect('instagram:feed')
    else:
        return render(request,'accounts/signup.html',{})

def logout(request):
    if request.method=='GET':
        auth.logout(request)
        return redirect('accounts:login')

def edit(request):
    return render(request,'accounts/edit.html',{'u':request.user,'p':profile.objects.get(user=request.user)})

def change_pro_pic(request,action):
    print(action)
    if action =="default_change":
        if request.method == 'POST':
            u = profile.objects.get(user=request.user)
            u.profile_pic = request.FILES['propic']
            u.save()
    elif action == "change":
        if request.method == 'POST':
            u = profile.objects.get(user=request.user)
            u.profile_pic.delete()
            u.profile_pic = request.FILES['propic']
            u.save()
    else:
        if request.method == 'POST':
            u = profile.objects.get(user=request.user)
            u.profile_pic.delete()
            u.profile_pic = 'defaultPic/default_profile_pic.jpg'
            u.save()
    return redirect('instagram:profile',u_name=u.user)