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
from django.db.models import Q


@login_required
def edit_profile(request):
    user = request.user  # Get the User instance
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        # Handle user information update
        if 'update_info' in request.POST:
            full_name = request.POST.get('full_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')

            # Split full name into first name and last name
            first_name, last_name = full_name.split() if ' ' in full_name else (full_name, '')

            # Update user information
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()
            user_profile.phone_number = phone_number
            user_profile.save()

        # Redirect to the profile page after saving changes
        return redirect('home:profile')

    return render(request, 'home/edit_profile.html', {'user': user, 'user_profile': user_profile})

@login_required(login_url='userprofile:signin')
def profile(request):
    user = request.user

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        # Retrieve values for other fields as needed

        user.first_name, user.last_name = full_name.split() if ' ' in full_name else (full_name, )
        user.username = username
        user.email = email
        # Update other fields here

        user.save()

        return JsonResponse({'success': True})

    return render(request, 'home/profile.html', {'user': user})

class CustomLogoutView(LogoutView):
    next_page = '/'

def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.select_related('laptopspec')
    
    # Define the variable 'filtered_products' before the 'if' block
    filtered_products = products

    if query:
        # Use Q objects to perform a case-insensitive search on multiple fields
        filtered_products = filtered_products.filter(
            Q(brand_name__icontains=query) |
            Q(model__icontains=query) |
            Q(laptopspec__cpu__icontains=query)
        )

    return render(request, 'home/product_list.html', {'products': filtered_products})



def product_list_ajax(request):
    query = request.GET.get('q')
    products = Product.objects.select_related('laptopspec')

    if query:
    # Use Q objects to perform a case-insensitive search on multiple fields
        products = products.filter(
        Q(brand_name__icontains=query) |
        Q(model__icontains=query) |
        Q(laptopspec__cpu__icontains=query)
        )

    search_results = []
    for product in products:
        search_results.append({
        'id': product.id,
        'brand_name': product.brand_name,
        'model': product.model,
        'cpu': product.laptopspec.cpu
    })

    return JsonResponse(search_results, safe=False)


def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    specs = LaptopSpec.objects.filter(product=product)

    image_fields = []
    for i in range(2, 7):
        field_name = f'image_{i}'
        image_field = getattr(product, field_name, None)
        if image_field:
            image_fields.append(image_field)

    # Add a query to get recommended products (you can customize this query)
    recommended_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:6]

    return render(request, 'home/product_details.html', {
        'product': product,
        'specs': specs,
        'recommended_products': recommended_products,
        'image_fields': image_fields
    })




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


    
