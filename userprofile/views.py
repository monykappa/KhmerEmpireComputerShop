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
from django.contrib import messages 



def custom_logout(request):
    logout(request)
    return redirect('userprofile:signin')


from django.contrib.auth import authenticate, login


def signin(request):
    if request.user.is_authenticated:
        return redirect('home:home')  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or protected view
            return redirect('home:home')
        else:
            # Handle authentication failure
            error_message = "Invalid username or password. Please try again."
    else:
        error_message = ""

    return render(request, 'userprofile/sign_in.html', {'error_message': error_message})

def signup(request):
    if request.user.is_authenticated:
        return redirect('home:home')  
    if request.method == 'POST':
        full_name = request.POST['full_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone_number = request.POST['phone-number']  # Get the phone number
        pfp = request.FILES.get('pfp')  # Get the profile picture file if provided

        # Split the full name into first name and last name
        first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')

        # Check if the passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        else:
            # Check if a user with the same username, email, or phone number already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken. Please choose a different one.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered. Please use a different email address.")
            elif UserProfile.objects.filter(phone_number=phone_number).exists():
                messages.error(request, "Phone number is already in use. Please use a different phone number.")
            else:
                # Create the user if the username, email, and phone number are unique
                user = User(username=username, email=email, password=make_password(password1))
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                # Create the UserProfile
                user_profile = UserProfile.objects.create(user=user, phone_number=phone_number)
                if pfp:
                    user_profile.profile_picture = pfp
                    user_profile.save()

                # Set the authentication backend
                user.backend = 'django.contrib.auth.backends.ModelBackend'

                # Log in the user
                login(request, user)
                messages.success(request, "Account created successfully.")
                return redirect('home:home')  # Redirect to your home page

    return render(request, 'userprofile/sign_up.html')