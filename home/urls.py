from django.urls import path, include
from . import views
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from .views import product_details, headphone_details


app_name = 'home'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('profile', views.profile, name='profile'),
    path('about_us', views.about_us, name='about_us'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', product_details, name='product_details'),
    path('headphone/<int:product_id>/', headphone_details, name='headphone_details'),
    path('logout/', LogoutView.as_view(next_page='home:index'), name='logout'),
    path('ajax/', views.product_list_ajax, name='product_list_ajax'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),

    #paypal url
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment_complete/', views.payment_complete, name='payment_complete'),
    path('payment-failed/', views.payment_failed_view, name='payment_failed'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    # path('checkout/<int:pk>/', views.checkout, name='checkout'),

    
    path('order-history/', views.order_history, name='order_history') 
    
    
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
