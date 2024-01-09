from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static


app_name = 'userprofile' 

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    # path('accounts/login/', CustomGoogleLoginView.as_view(), name='custom_google_login'),
    path('signup/', views.signup, name='signup'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)