from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render(request, 'index.html')

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('account')
        
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'user/login.html')

def logoutUser(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('index')

def signupUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account created!')
            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'An error has occurred during registration')
            return redirect('signup')
    context = {'form': form}
    return render(request, 'user/signup.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    items = profile.item_set.all()

    context = {'profile': profile, 'items': items}
    return render(request, 'user/account.html', context)


