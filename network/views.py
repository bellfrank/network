from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.list import ListView

from .models import User, Posts
from django import forms


def index(request):
    posts = Posts.objects.all()

    # Set up Pagination
    paginator = Paginator(posts, 10) # show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html",{
        "posts":posts,
        "page_obj":page_obj,
    })

@login_required
def profile(request, name):
    # fetching the profile users posts
    posts = User.objects.get(username=name).user_post.all()
    number_posts = len(posts)

    # determining who the logged in user follows
    following = User.objects.get(username=request.user).followees.all()
    name1 = User.objects.get(username=name)
    
    # follow and unfollow button logic, if logged in user follows, then unfollow button is active
    follow = False
    if name1 in following:
        follow = True
        
    # user clicks follow/unfollow button
    if request.method == "POST":
        # getting the user object
        user = User.objects.get(id=request.user.id)
        id = User.objects.get(username=name).id
        # person clicked unfollow, else clicked follow
        if follow:
            remove_follower = user.followees.remove(id)
            follow = False
        else:
            add_follower = user.followees.add(id)
            follow = True

        return HttpResponseRedirect(reverse('profile', args=[str(name)]))
        

    else:
        return render(request, "network/profile.html",{
            "posts":posts,
            "name":name,
            "number_posts":number_posts,
            "follow":follow,
        })

@login_required
def create(request):
    #DEBUG

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
    
    following = User.objects.get(username=request.user).followees.all()
    
    # getting all the posts and in HTML using python filter the correct posts
    posts = Posts.objects.all()

    return render(request, "network/following.html",{
        "followers":followers,
        "following":following,
        "posts":posts,
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




class PageList(ListView):
    paginate_by = 10
    model = Posts

#FORMS
class PostForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Posts
        fields = ( 'description',)
        
        widgets = {
            'description': forms.Textarea(attrs={'class':'form-control'}),
        }