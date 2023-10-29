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
from userprofile.models import *
from django.contrib.auth.views import LogoutView
from .forms import UserProfileForm

@login_required(login_url='userprofile:signin') 
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # If the user's profile doesn't exist, create one
        user_profile = UserProfile(user=request.user)
        user_profile.save()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'home/profile.html', {'user_profile': user_profile, 'form': form})

class CustomLogoutView(LogoutView):
    next_page = '/'

def product_list(request):
    products = Product.objects.select_related('laptopspec').all()
    return render(request, 'home/product_list.html', {'products': products})



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


    
