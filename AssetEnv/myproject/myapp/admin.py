from django.contrib import admin

# Register your models here.

from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
 
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_verified', 'one_time_token')}),
    )
 
admin.site.register(CustomUser, CustomUserAdmin)
