from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, Posts
from django import forms


def index(request):
    posts = Posts.objects.all()

    return render(request, "network/index.html",{
        "posts":posts,
    })

@login_required
def profile(request, user):
    posts = User.objects.get(username=user).user_post.all()
    number_posts = len(posts)
    print(request.user)
    print(user)
    if request.method == "POST":
        following = User.objects.get(username=request.user).following.all()
        print(following)
        if(user in following):
            print("true")
        return render(request, "network/profile.html",{
            "posts":posts,
            "user":user,
            "number_posts":number_posts,
        })
        
    else:
        return render(request, "network/profile.html",{
            "posts":posts,
            "user":user,
            "number_posts":number_posts,
        })

@login_required
def create(request):
    #DEBUG
    print("Inside Create")

    if request.method == "POST":
        form = PostForm(request.POST)
        form.instance.user = request.user
        
        if form.is_valid():
            form.save()
            messages.success(request, ('Your post was succesfull!'))
            return HttpResponseRedirect(reverse("index"))


    else:
        return render(request, "network/create.html",{
        "PostForm":PostForm(),
    })

@login_required
def following(request):

    followers = User.objects.get(username=request.user).followers.all()
    
    # this method required turning symmetry methods to false
    following = User.objects.get(username=request.user).followees.all()
    # following = User.objects.get(username=request.user).following.all()

   
    return render(request, "network/following.html",{
        "followers":followers,
        "following":following,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")





#FORMS
class PostForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Posts
        fields = ( 'description',)
        
        widgets = {
            'description': forms.Textarea(attrs={'class':'form-control'}),
        }