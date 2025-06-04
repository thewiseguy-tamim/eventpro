from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not first_name or not last_name:
            raise ValueError('First name and last name must be set')
        user = self.model(username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password, **extra_fields):
        if not username:
            raise ValueError('Superuser must have a username.')
        if not first_name or not last_name:
            raise ValueError('Superuser must have first_name and last_name.')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, first_name, last_name, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('client', 'Client'),
    )
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)  # Email optional
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"