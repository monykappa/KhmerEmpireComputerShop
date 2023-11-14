from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

app_name = 'home'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('profile', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.laptop_details, name='laptop_details'),
    path('product/<int:product_id>/', views.headphone_details, name='headphone_details'),
    path('logout/', LogoutView.as_view(next_page='home:index'), name='logout'),
    path('ajax/', views.product_list_ajax, name='product_list_ajax'),
    
    # Add more URL patterns as needed
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
