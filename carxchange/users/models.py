from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from carseller.models import Car
from .choices import REGION_CHOICES


class CarUser(AbstractUser):
    full_name = models.CharField(max_length=50)
    fav_sellers = models.ManyToManyField(settings.AUTH_USER_MODEL)
    fav_cars = models.ManyToManyField(Car)
    region = models.CharField(max_length=3, choices=REGION_CHOICES)
    contacts = models.CharField(max_length=150)
    picture = models.ImageField(upload_to='profile_pictures/')