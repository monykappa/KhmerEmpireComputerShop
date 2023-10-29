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
    path('products/', views.product_list, name='product_list'),
    path('logout/', LogoutView.as_view(next_page='home:index'), name='logout'),
    
    # Add more URL patterns as needed
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
