from rest_framework import serializers
from django.contrib.auth import get_user_model

from carseller.choices import (WHEEL_CHOICES, FUEL_CHOICES, 
                    ACCIDENTS_CHOICES, BRAND_CHOICES, TRANS_CHOICES)
from carseller.models import Car


user_model = get_user_model()


class CarSerializer(serializers.ModelSerializer):

    # photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'title', 'price', 'runtime', 'color', 'owner', 'fuel',
                  'description', 
                  'wheel', 'accidents', 'brand', 'transmission', 'picture']
        readonly = ["create_time"]
        
    # def validate_fuel(self, value):
    #     print(value)
    #     choices = [c[0] for c in FUEL_CHOICES]
    #     print(choices)
    #     if value not in choices:
    #         f_c = ''
    #         for choice in FUEL_CHOICES:
    #             f_c += f'{choice[0]} - {choice[1]} '
    #         raise serializers.ValidationError('Available choices are' + f_c)
    #     return value
    

class UserSerializer(serializers.ModelSerializer):

    # photo_url = serializers.SerializerMethodField()

    class Meta:
        model = user_model
        fields = ['id', 'full_name', 'region', 'picture',
                  'contacts', 'cars_added']
        
    # def get_photo_url(self, user):
    #     request = self.context.get('request')
    #     print(user)
    #     photo_url = user.picture.url
    #     return request.build_absolute_uri(photo_url)
