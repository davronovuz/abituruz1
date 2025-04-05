from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(UserConfirmation)
class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'auth_status', 'is_confirmed', 'attempts']
    list_filter = ['user', 'auth_status', 'is_confirmed', 'attempts']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'user_role', 'status', 'avatar']
    list_filter = ['user_role', 'status']
