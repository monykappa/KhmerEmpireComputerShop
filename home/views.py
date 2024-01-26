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
from django.utils import timezone
from userprofile.models import *
from django.contrib.auth.views import LogoutView
from .forms import UserProfileForm
from django.db.models import Q
from decimal import Decimal
from embed_video.templatetags.embed_video_tags import register
from django.views.decorators.http import require_POST
from .forms import *
import json




def about_us(request):
    return render(request, 'home/about_us.html')
def order_history(request):
    orders = OrderHistory.objects.filter(user=request.user).order_by('-id')
    context = {'orders': orders}
    return render(request, 'home/order_history.html', context)


def clear_cart(request):
    # Get cart items
    cart_items = CartItem.objects.filter(order__user=request.user)
    
    # Calculate total
    total = sum(item.subtotal for item in cart_items)
    
    # Create OrderHistory
    order_history = OrderHistory.objects.create(
        user=request.user, 
        total_price=total
    )

    # Save items
    for item in cart_items:
        OrderHistoryItem.objects.create(
            order_history=order_history,
            product=item.product,
            quantity=item.quantity,
            subtotal=item.subtotal
            )

    # Clear cart 
    CartItem.objects.filter(order__user=request.user).delete()

    # Redirect
    return redirect('home:payment_complete') 

    
#Paypal payment integration
def payment_complete(request):
    # Get the most recent order for the user
    order_history = OrderHistory.objects.filter(user=request.user).order_by('-id').first()
    order_history = {'order_history': order_history}

    # Alternatively, you can use get_object_or_404 to handle the case where no order is found
    # order = get_object_or_404(Order, user=request.user)

    return render(request, 'payment/payment_completed.html', {'order_history': order_history}, )

def payment_failed_view(request):
    return render(request, 'payment/payment_failed.html')

# @login_required
# def checkout(request, pk):
#     cart_item = CartItem.objects.get(id=pk, order__user=request.user)

#     # Debug statement to check cart_item.pk value
#     print("Cart Item PK:", cart_item.pk)

#     context = {'cart_item': cart_item}
#     return render(request, 'payment/checkout.html', context)



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    current_time = timezone.now()

    # Get the quantity from the query parameters
    quantity = int(request.GET.get('quantity', 1))

    try:
        # Check if there is an existing open order for the user within the last 5 minutes
        existing_order = Order.objects.filter(user=user, total_price=0.0, created_at__gte=current_time - timezone.timedelta(minutes=5)).first()

        if existing_order:
            order = existing_order
        else:
            # If no existing order, create a new order
            order = Order.objects.create(user=user, total_price=0.0)

        # Calculate the total quantity in the cart for the specific product
        total_quantity_in_cart = order.cartitem_set.filter(product=product).aggregate(models.Sum('quantity'))['quantity__sum'] or 0

        if product.stock.quantity >= quantity:
            # Check if the product is already in the cart
            cart_item, cart_item_created = CartItem.objects.get_or_create(order=order, product=product)

            if not cart_item_created:
                # Calculate the quantity to add to the existing quantity in the cart
                additional_quantity = quantity - cart_item.quantity
                cart_item.quantity += additional_quantity
                cart_item.subtotal = product.price * cart_item.quantity
                cart_item.save()
            else:
                # Set quantity and subtotal
                cart_item.quantity = quantity
                cart_item.subtotal = product.price * quantity
                cart_item.save()

            # Update stock quantity based on the requested quantity
            product.stock.quantity = max(0, product.stock.quantity - quantity)
            product.stock.save()

            # Update total price of the order
            order.total_price = sum(item.subtotal for item in order.cartitem_set.all())
            order.save()

            return JsonResponse({'message': f'{product.name} added to cart, quantity: {quantity}'})
        else:
            raise ValueError("Insufficient stock")
    except Stock.DoesNotExist:
        raise ValueError("Stock does not exist for the product")



def cart(request):
    if request.method == 'POST' and 'paypal' in request.POST:
        # Process PayPal payment and capture details here

        # Clear the user's cart after successful payment
        user_cart_items = CartItem.objects.filter(order__user=request.user)
        user_cart_items.delete()

        return redirect('home:cart')  # Redirect to a success page after payment

    user_cart_items = CartItem.objects.filter(order__user=request.user)
    total_price = sum(item.subtotal for item in user_cart_items)

    return render(request, 'home/cart.html', {'cart_items': user_cart_items, 'total_price': total_price})


def remove_from_cart(request):
    if request.method == 'POST':
        form = RemoveFromCartForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data['item_id']
            item = get_object_or_404(CartItem, id=item_id)

            # Update the stock when removing a product from the cart
            stock = get_object_or_404(Stock, product=item.product)
            stock.quantity += item.quantity
            stock.save()

            # Perform the logic to remove the item from the cart
            item.delete()

            return redirect('home:cart')

    # Redirect back to the cart page if the form is not valid
    return redirect('home:cart')


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




#Product list page
def product_list(request):
    query = request.GET.get('q')
    
    laptop_stocks = Stock.objects.filter(product__category__name='Laptop').select_related('product__laptopspec')
    headphone_stocks = Stock.objects.filter(product__category__name='Headphone').select_related('product__headphonespec')

    if query:
        laptop_stocks = laptop_stocks.filter(
            Q(product__brand_name__icontains=query) |
            Q(product__model__icontains=query) |
            Q(product__laptopspec__cpu__icontains=query)
        )
        
        headphone_stocks = headphone_stocks.filter(
            Q(product__brand_name__icontains=query) |
            Q(product__model__icontains=query) |
            Q(product__headphonespec__driver_size__icontains=query)
        )

    return render(request, 'products/product_list.html', {'laptop_stocks': laptop_stocks, 'headphone_stocks': headphone_stocks})



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


def headphone_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    specs = HeadphoneSpec.objects.filter(product=product).first() 

    stock = Stock.objects.filter(product=product).first()

    image_fields = []
    for i in range(2, 7):
        field_name = f'image_{i}'
        image_field = getattr(product, field_name, None)
        if image_field:
            image_fields.append(image_field)

    recommended_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:6]

    return render(request, 'products/headphone_details.html', {
        'product': product,
        'specs': specs,
        'stock': stock,
        'recommended_products': recommended_products,
        'image_fields': image_fields
    })



def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    specs = LaptopSpec.objects.filter(product=product)
    
    # Fetch the stock for the given product
    stock = Stock.objects.filter(product=product).first()

    image_fields = []
    for i in range(2, 7):
        field_name = f'image_{i}'
        image_field = getattr(product, field_name, None)
        if image_field:
            image_fields.append(image_field)

    # Add a query to get recommended products (you can customize this query)
    recommended_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:6]

    return render(request, 'products/laptop_details.html', {
        'product': product,
        'specs': specs,
        'stock': stock,  # Pass the stock to the template
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


    
