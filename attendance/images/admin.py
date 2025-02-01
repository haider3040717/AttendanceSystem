from django.contrib import admin
from .models import Image


# Register your models here.

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  # Number of empty forms to display


admin.site.register(Image)
