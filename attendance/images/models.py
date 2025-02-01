from PIL import Image as PilImage
from django.db import models
from django.utils.text import slugify
import os
from account.models import CustomUser


# Create your models here.

def upload_to(instance, filename):
    new_filename = f"{filename}"
    return os.path.join('images/', new_filename)


class Image(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to, default='images/default-profile.png')
    # image = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return self.image.name
