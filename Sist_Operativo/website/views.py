from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_control
from django.contrib import messages

from .forms import RegisterForm
from .forms import TokenForm
from .tokens import Token


# Create your views here.

User = get_user_model()

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def home(request):
    if not request.user.is_authenticated:
        redirect('login')
    username = request.user
    context = {
        "username": username,
    }
    return render(request, "website/index.html", context)

# Register View
def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
               form.save()
               return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error) 
    else:
        form = RegisterForm()
    context = {
        'form':form,
    }
    return render(request, 'website/register.html', context)

# Login View
def login_page(request):
    form = AuthenticationForm()
    token = Token()

    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token_gen = token.token_gen()
            email = request.user.email
            token.send_mail(email, token_gen)
            
            request.session['auth_token'] = token_gen
            return redirect('auth')
        else:
            messages.error(request,"Usuario o contraseña invalido")
    context = {
        'form':form,
    }
    return render(request, 'website/login.html', context)

# Auth View
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def auth_page(request):
    form = TokenForm()
    auth_token = request.session['auth_token']

    if request.method == 'POST':
        form = TokenForm(request.POST)
        form_token = request.POST.get('token')

        if form.is_valid() and len(form_token) == 6:        
            if form_token == auth_token:      
                return redirect('home')
            else:
                 messages.error(request,"Token invalido")
        else:
            messages.error(request,"Token invalido")
    context = {
        'form':form,
    }
    return render(request, 'website/auth.html', context)

# logout 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')

# Resend Token
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def resend_token(request):
    token = Token()
    email = request.user.email
    auth_token = request.session['auth_token']
    token.send_mail(email, auth_token)
    return redirect('auth')