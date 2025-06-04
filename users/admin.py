from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_picture', 'address', 'phone_number')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'is_active', 'is_staff'),
        }),
    )

    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

admin.site.register(User, UserAdmin)