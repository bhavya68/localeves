
import uuid
from django.db import models
# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('An email address is required to create a user')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', 'normal')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('normal', 'Normal User'),
       

        ('guest_owner', 'Guest Owner'),
        

        ('owner', 'Verified Owner'),
    ]
    email = models.EmailField(
        unique=True,  
    )
    username = models.CharField(
        max_length=50,
        unique=True,
        blank=False,)
    full_name = models.CharField(
        max_length=150,
        blank=True,)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True,)
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='normal',)
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,)
    is_active = models.BooleanField(
        default=True,)
    is_staff = models.BooleanField(
        default=False,)
    guest_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        null=True,
        blank=True,)
    created_at = models.DateTimeField(
        auto_now_add=True,)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['full_name', 'username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name or self.email
       

    def get_short_name(self):
        if self.full_name:
            return self.full_name.split()[0]
        return self.username
        

    def is_verified_owner(self):
        return self.user_type == 'owner'
       

    def is_guest_owner(self):
        return self.user_type == 'guest_owner'

    def is_normal_user(self):
        return self.user_type == 'normal'
    