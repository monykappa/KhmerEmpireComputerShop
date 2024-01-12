from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import uuid
from django.core.exceptions import ValidationError
import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.utils import timezone


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def user_directory_path(instance, filename):
    # Generate a unique identifier for the directory
    unique_id = str(uuid.uuid4())
    # Construct the directory path
    directory_path = f'content/{unique_id}/'

    # Return the complete file path
    return os.path.join(directory_path, filename)




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=user_directory_path, validators=[validate_file_extension], blank=True, null=True)
    other_field = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username