from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
import json

@csrf_exempt
def post_list_create(request):
    if request.method == 'GET':
        posts = list(Post.objects.values())
        return JsonResponse(posts, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        post = Post.objects.create(**data)
        return JsonResponse({'id': post.id, 'title': post.title, 'content': post.content})

@login_required
def dashboard(request):
    # Fetch posts created by the logged-in user
    posts = Post.objects.filter(author=request.user)
    return render(request, 'dashboard.html', {'posts': posts})

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('dashboard')  # Redirect to the dashboard after saving
    else:
        form = PostForm()
    
    return render(request, 'add_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.author == request.user:  # Ensure only the author can delete the post
        post.delete()
    return redirect('dashboard')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html') 

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have logged in successfully!')
            # Redirect to the dashboard (or homepage)
            return redirect('dashboard')  # or 'home' if you want the home page
        else:
            messages.error(request, 'Invalid credentials, please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Dashboard view (after login success)
def dashboard_view(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()  # Retrieve all posts, or just the user's posts
        return render(request, 'dashboard.html', {'posts': posts})
    else:
        return redirect('login')  # Redirect to login page if not authenticated

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assign the logged-in user as the author
            post.save()
            return redirect('dashboard')  # Redirect to the dashboard after saving
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def edit_post(request, id):
    # Fetch the post object by its ID
    post = get_object_or_404(Post, id=id)

    # Check if the current user is the author of the post
    if post.author != request.user:
        return redirect('dashboard')  # Optionally, redirect if they are not the author

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()  # Save the updated post
            return redirect('dashboard')  # Redirect after saving
    else:
        form = PostForm(instance=post)  # Pre-fill the form with the post's data

    return render(request, 'edit_post.html', {'form': form, 'post': post})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have logged out successfully!')
    return redirect('login')  # Redirect to login page after logout

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Check if the username or email already exists
            if User.objects.filter(username=name).exists():
                form.add_error('name', 'Username already exists.')
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                form.add_error('email', 'Email is already registered.')
                messages.error(request, 'Email is already registered.')
            else:
                # If no user exists with the same name or email, create the user
                user = User.objects.create_user(username=name, email=email, password=password)

                # You can also set additional fields, e.g. first_name, last_name if necessary
                # user.first_name = 'Some Name'  # if you have additional fields for user
                # user.save()

                messages.success(request, 'Your account has been successfully created! Please log in.')
                return redirect('home')  # Redirect to the login page after successful registration
        else:
            # If the form is invalid, re-render the registration page with errors
            messages.error(request, 'There was an error with your registration. Please check your inputs.')
            return render(request, 'home.html', {'form': form})

    else:
        form = RegistrationForm()  # Empty form for GET request
        return render(request, 'home.html', {'form': form})
