from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Show these fields in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'position', 'is_superuser', 'profile_photo_tag')
    list_filter = ('role', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'position', 'phone_number')

    # Fieldsets for user detail page in admin
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_photo', 'position')}),
        ('Roles & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to show when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'position', 'profile_photo', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')

    @admin.display(description="Profile Photo")
    def profile_photo_tag(self, obj):
        if obj.profile_photo:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:50%;" />',
                obj.profile_photo.url
            )
        return ""
