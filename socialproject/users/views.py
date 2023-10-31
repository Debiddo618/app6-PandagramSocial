from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegisterForm, UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile
from posts.models import Post
from django.contrib import messages


# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data["username"], password=data["password"])

            if user is not None:
                login(request, user)
                # change here to change login
                messages.success(request, 'User authenticated and logged in.')
                return redirect('feed')
            else:
                messages.success(request,"Invalid credentials")
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


@login_required()
def index(request):
    logged_user = request.user
    profile = Profile.objects.filter(user=logged_user).first
    posts = Post.objects.filter(user=logged_user)
    return render(request, "users/index.html", {'posts': posts, "profile":profile, "logged_user":logged_user})


def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, "users/register_done.html")
    else:
        user_form = UserRegisterForm()
    return render(request, "users/register.html", {"user_form": user_form})


@login_required()
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, "users/edit.html", {"user_form": user_form, "profile_form": profile_form})
