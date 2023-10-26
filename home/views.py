from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User 
from django.contrib.auth import logout
from .models import *
from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    next_page = '/'

def product(request):
    template = 'home/product.html'
    return render(request, template)


@login_required(login_url='userprofile:signin')  # Use the view name 'userprofile:signin'
def home(request):
    template = 'home/home.html'
    return render(request, template)
    
@login_required(login_url='userprofile:signin')  # Use the view name 'userprofile:signin'
def base(request):
    template = 'home/base.html'
    return render(request, template)

def index(request):
    templates = 'home/index.html'
    return render(request, templates)


    
