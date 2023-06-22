from rest_framework import serializers
from carseller.models import Car
from django.contrib.auth import get_user_model

user_model = get_user_model()


class CarSerializer(serializers.ModelSerializer):

    # photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'title', 'price', 'runtime', 'color', 'owner', 'fuel',
                  'description', 
                  'wheel', 'accidents', 'brand', 'transmission', 'picture']
        readonly = ["create_time"]
        
    # def get_photo_url(self, car):
    #     request = self.context.get('request')
    #     photo_url = car.picture.url
    #     return request.build_absolute_uri(photo_url)
    

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
