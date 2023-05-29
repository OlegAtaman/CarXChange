from random import randrange
from django.core.files import File

import choices as ch
from models import Car
from users.models import CarUser
from users.choices import REGION_CHOICES


letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '

def get_string(length, with_space=False):
    string = ''
    if with_space:
        for i in range(length):
            string += letters[randrange(len(letters))]
    else:
        for i in range(length):
            string += letters[randrange(len(letters)-1)]
    return string

for i in range(50):
    user = CarUser(username=get_string(15), password='K'+get_string(15)+'1', 
                   full_name=get_string(20), region=REGION_CHOICES[randrange(len(REGION_CHOICES))][0],
                   contacts=get_string(30), email=get_string(15)+'@gmail.com'
                   )
    user.picture.save(get_string(10)+'.png', File(open('/carxchange/media/profile_pictures/sellersample.jpeg', 'r')))
    user.save()

users = CarUser.objects.filter(is_staff=False)

for i in range(300):
    car = Car(title=get_string(15), price=randrange(1500000), runtime=randrange(1000000),
              color=get_string(2), wheel=ch.WHEEL_CHOICES[randrange(len(ch.WHEEL_CHOICES))][0],
              fuel=ch.FUEL_CHOICES[randrange(len(ch.FUEL_CHOICES))][0],
              accidents=ch.ACCIDENTS_CHOICES[randrange(len(ch.ACCIDENTS_CHOICES))][0],
              brand=ch.BRAND_CHOICES[randrange(len(ch.BRAND_CHOICES))][0],
              transmission=ch.TRANS_CHOICES[randrange(len(ch.TRANS_CHOICES))][0],
              description=get_string(100, True), owner=users[randrange(len(users))])
    car.picture.save(get_string(10)+'.png', File(open('/carxchange/media/car_pictures/car.png', 'r')))
    car.save()

