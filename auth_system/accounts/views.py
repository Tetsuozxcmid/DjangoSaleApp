from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm,PostForm
from .models import Post

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('auth_login')
        else:
            messages.error(request,'Registration failed')
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form':form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('auth_welcome')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')

    else:
        form = AuthenticationForm()
    return render(request,'login.html',{'form':form})

@login_required
def welcome(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request,'index.html',{'posts':posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('auth_welcome')
    else:
        form = PostForm()
    return render(request,'create_post.html',{'form': form})

def logout_view(request):
    logout(request)
    return redirect('auth_login')
                
            