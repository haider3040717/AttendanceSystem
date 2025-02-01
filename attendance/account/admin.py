from django.contrib import admin
from .models import CustomUser


# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'date_joined')


admin.site.register(CustomUser, CustomUserAdmin)