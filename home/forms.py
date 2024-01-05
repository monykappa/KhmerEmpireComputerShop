from django import forms
from .models import User
from django.contrib.auth.forms import UserChangeForm
from userprofile.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'profile_picture', 'other_field']
        

class RemoveFromCartForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())



