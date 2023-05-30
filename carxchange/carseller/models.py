from django.db import models
from django.conf import settings

from .choices import (WHEEL_CHOICES, FUEL_CHOICES, 
                    ACCIDENTS_CHOICES, BRAND_CHOICES, TRANS_CHOICES)


class Car(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    runtime = models.DecimalField(max_digits=10, decimal_places=3)
    color = models.CharField(max_length=30)
    wheel = models.CharField(max_length=3, choices=WHEEL_CHOICES)
    fuel = models.CharField(max_length=3, choices=FUEL_CHOICES)
    accidents = models.CharField(max_length=3, choices=ACCIDENTS_CHOICES)
    brand = models.CharField(max_length=3, choices=BRAND_CHOICES)
    transmission = models.CharField(max_length=3, choices=TRANS_CHOICES)
    description = models.TextField(max_length=1000)
    picture = models.ImageField(upload_to='car_pictures/')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_time = models.TimeField(auto_now=True)