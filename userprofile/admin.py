from django.contrib import admin
from .models import * 
from django.utils.html import format_html




class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_profile_picture', 'other_field')

    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="max-width: 120px; max-height: 120px; object-fit: cover;" />', obj.profile_picture.url)
        return "No Image"

    display_profile_picture.short_description = 'Profile Picture'

# Register the UserProfile model with its admin class
admin.site.register(UserProfile, UserProfileAdmin)
