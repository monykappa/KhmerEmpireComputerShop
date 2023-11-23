from django.urls import path
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
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', product_details, name='product_details'),
    path('headphone/<int:product_id>/', headphone_details, name='headphone_details'),
    path('logout/', LogoutView.as_view(next_page='home:index'), name='logout'),
    path('ajax/', views.product_list_ajax, name='product_list_ajax'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/<int:quantity>/', views.add_to_cart, name='add_to_cart'),


    
    # Add more URL patterns as needed
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
