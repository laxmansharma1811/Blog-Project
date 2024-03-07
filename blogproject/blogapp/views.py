from django.shortcuts import render, get_object_or_404,redirect,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError


# Create your views here.
@login_required(login_url='login')
def home(request):
    blogs = Blog.objects.all()
    return render(request, 'home.html', {'blogs':blogs})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            return HttpResponseRedirect(reverse('login'))
        except IntegrityError:
            # Handle duplicate username error here
            # For example, display an error message to the user
            error_message = "Username '{}' already exists. Please choose a different username.".format(username)
            return render(request, 'register.html', {'error_message': error_message})

    return render(request, 'register.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='login')
def add_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if title and content:
            Blog.objects.create(title=title, content=content, image=image, author=request.user)
            return HttpResponseRedirect(reverse('home'))

    return render(request, 'add_blog.html')




@login_required(login_url='login')
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.user != blog.author:
        messages.error(request, "You don't have permission to edit this blog.")
        return redirect('home')
    
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        new_image = request.FILES.get('image')

        if new_image:
            blog.image = new_image

        blog.save()
        return redirect('home')
    else:
        return render(request, 'edit_blog.html', {'blog': blog})


@login_required(login_url='login')
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.user != blog.author:
        messages.error(request, "You don't have permission to edit this blog.")
        return redirect('home')

    if request.method == 'POST':
        blog.delete()
        return redirect('home')

    return render(request, 'delete_blog.html', {'blog': blog})


#Like blog
@login_required(login_url='login')
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)

    return redirect(reverse('home'))



#Comment
from django.utils import timezone
@login_required(login_url='login')
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            comment = Comment.objects.create(user=request.user, blog=blog, content=content, created_at=timezone.now())
            return redirect(reverse('home'))

    return render(request, 'add_comment.html', {'blog': blog})