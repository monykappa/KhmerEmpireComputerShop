from django.contrib import admin
from .models import UserProfile  # Import the UserProfile model from your models.py

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture', 'other_field')

# Register the UserProfile model with its admin class
admin.site.register(UserProfile, UserProfileAdmin)

