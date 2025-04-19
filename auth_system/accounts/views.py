from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, PostForm, ExchangeOfferForm
from .models import Post, Offer
from django.db.models import Q
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('auth_login')
        else:
            messages.error(request, 'Registration failed')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
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
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def welcome(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'accounts/index.html', {'posts': posts})


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
    return render(request, 'accounts/create_post.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, "Обьявление успешно изменено")
                return redirect('auth_welcome')
        else:
            form = PostForm(instance=post)
    else:
        messages.error(
            request, "Вы можете редактировать только свои обьявления")
    return render(request, 'accounts/edit_post.html', {'form': form, 'post': post})


@login_required
def logout_view(request):
    logout(request)
    return redirect('auth_login')


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('auth_welcome')


@login_required
def create_exchange_offer(request, post_id):
    sender_post = get_object_or_404(Post, id=post_id)
    if sender_post.author == request.user:
        messages.error(
            request, "Вы не можете предложить обмен своего же объявления!")
        return redirect('post_detail', post_id=post_id)

    if request.method == 'POST':
        form = ExchangeOfferForm(request.POST, user=request.user)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.sender_user = request.user
            offer.ad_receiver = sender_post
            offer.save()
            messages.success(request, 'Предложение обмена отправлено!')
            return redirect('auth_welcome')
    else:

        form = ExchangeOfferForm(user=request.user, initial={
                                 'ad_receiver': sender_post})

    return render(request, 'accounts/create_offer.html', {
        'form': form,
        'sender_post': sender_post
    })


@login_required
def user_offers(request):
    offers = Offer.objects.filter(ad_receiver__author=request.user)
    return render(request, 'accounts/user_offers.html', {'offers': offers})


@login_required
def accept_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    if request.method == 'POST':
        offer.status = 'accepted'
        offer.save()
        messages.success(request, 'Предложение принято!')
        return redirect('auth_welcome')
    return redirect('accept_offer')


@login_required
def reject_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    if request.method == 'POST':
        offer.status = 'rejected'
        offer.save()
        messages.success(request, 'Предложение отклонено!')
        return redirect('auth_welcome')
    return redirect('reject_offer')


def searching(request):
    search_query = request.GET.get('search', '')

    posts = Post.objects.all()

    if search_query:
        posts = posts.filter(Q(title__icontains=search_query.strip()) | Q(
            description__icontains=search_query.strip()))

    posts = posts.order_by('-created_at')

    context = {
        'posts': posts,
        'search_query': search_query,

    }
    return render(request, 'accounts/index.html', context)
