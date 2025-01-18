from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Customize the display of the CustomUser model in the admin interface
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Fields to display in the admin list view
    list_display = ['username', 'email', 'phone_number', 'is_staff']
    # Fields to search in the admin interface
    search_fields = ['username', 'email', 'phone_number']
    # Fields to display in the detail view
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    # Fields to include in the add user form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'email')}),
    )

# Register the CustomUser model with the admin interface
admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
