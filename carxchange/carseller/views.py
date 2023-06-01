from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from random import randrange
from django.core.files import File
from django.db.models import Q
from django.http import HttpResponseForbidden, JsonResponse
import json


from .filter import filter
from django.conf import settings
from .models import Car
from .forms import CarForm
import carseller.choices as ch
from users.choices import REGION_CHOICES
from users.models import CarUser


def index(request):
    return render(request, 'carseller/index.html')

def profile(request):
    user = request.user
    cars = Car.objects.filter(owner=user)
    count = len(cars)
    ctx = {
        'reg_choices': REGION_CHOICES,
        'seller': user,
        'cars': cars,
        'car_count': count
    }
    return render(request, 'carseller/profile.html', ctx)

class NewCarAdd(View):
    template = 'carseller/newadd.html'
    
    def get(self, request):
        ctx = {
            'form':CarForm()
        }
        return render(request, self.template, ctx)

    def post(self, request):
        form = CarForm(request.POST, request.FILES)

        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            car.owner.cars_added += 1
            car.owner.save()
            return redirect('profile')

        ctx = {"form": form}
        return render(request, self.template, ctx)

def sellerview(request, pk):
    user_model = get_user_model()
    seller = user_model.objects.get(id=pk)
    cars = Car.objects.filter(owner=seller)
    count = len(cars)
    ctx = {
        'seller': seller,
        'cars': cars,
        'car_count': count
    }
    return render(request, 'carseller/seller.html', ctx)

def carview(request, pk):
    car = Car.objects.get(id=pk)
    return render(request, 'carseller/carview.html', {'car':car})

def carlist(request):
    favsearch = False
    cars = Car.objects.all()
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 1
    if request.GET.get('fav'):
        cars = request.user.fav_cars.all()
        favsearch = True
    cars = filter(cars, request.GET)
    pages = len(cars)//10+1
    cars = cars[10*(page-1):10*page]
    favs = []
    for car in cars:
        if car in request.user.fav_cars.all():
            favs.append(car)
    ctx = {
        'fav': favsearch,
        'fav_cars': favs,
        'page': page,
        'prev': page-1,
        'next': page+1,
        'pages': pages,
        'cars': cars,
        'fuel_choices': ch.FUEL_CHOICES,
        'accident_choices': ch.ACCIDENTS_CHOICES,
        'trans_choices': ch.TRANS_CHOICES,
        'brand_choices': ch.BRAND_CHOICES,
        'wheel_choices': ch.WHEEL_CHOICES
    }
    return render(request, 'carseller/cars.html', ctx)

def sellerlist(request):
    favsearch = False
    user_model = get_user_model()
    sellers = user_model.objects.filter(is_staff=False)
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 1
    if request.GET.get('fav'):
        sellers = request.user.fav_sellers.all()
        favsearch = True
    if request.GET.get('search'):
        search = request.GET.get('search')[0].lower()
        search_filter = Q(full_name__icontains=search)
        search_filter.add(Q(region__icontains=search), Q.OR)
        search_filter.add(Q(contacts__icontains=search), Q.OR)
        sellers = sellers.filter(search_filter)
    pages = len(sellers)//15+1
    sellers = sellers[15*(page-1):15*page]
    favs = []
    for seller in sellers:
        if seller in request.user.fav_sellers.all():
            favs.append(seller)
    ctx = {
        'fav': favsearch,
        'fav_sellers': favs,
        'prev': page-1,
        'next': page+1,
        'page': page,
        'pages': pages,
        'sellers': sellers
    }
    return render(request, 'carseller/sellers.html', ctx)

def fill_db_view(request):
    
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '

    # def get_string(length, with_space=False):
    #     string = ''
    #     if with_space:
    #         for i in range(length):
    #             string += letters[randrange(len(letters))]
    #     else:
    #         for i in range(length):
    #             string += letters[randrange(len(letters)-1)]
    #     return string

    # for i in range(50):
    #     user = CarUser(username=get_string(15), password='K'+get_string(15)+'1', 
    #                 full_name=get_string(20), region=REGION_CHOICES[randrange(len(REGION_CHOICES))][0],
    #                 contacts=get_string(30), email=get_string(15)+'@gmail.com'
    #                 )
    #     user.picture.save(get_string(10)+'.png', File(open(settings.MEDIA_ROOT + '/profile_pictures/sellersample.jpeg', 'rb')))
    #     user.save()

    # users = CarUser.objects.filter(is_staff=False)

    # for i in range(300):
    #     car = Car(title=get_string(15), price=randrange(1500000), runtime=randrange(1000000),
    #             color=get_string(2), wheel=ch.WHEEL_CHOICES[randrange(len(ch.WHEEL_CHOICES))][0],
    #             fuel=ch.FUEL_CHOICES[randrange(len(ch.FUEL_CHOICES))][0],
    #             accidents=ch.ACCIDENTS_CHOICES[randrange(len(ch.ACCIDENTS_CHOICES))][0],
    #             brand=ch.BRAND_CHOICES[randrange(len(ch.BRAND_CHOICES))][0],
    #             transmission=ch.TRANS_CHOICES[randrange(len(ch.TRANS_CHOICES))][0],
    #             description=get_string(100, True), owner=users[randrange(len(users))])
    #     car.picture.save(get_string(10)+'.png', File(open(settings.MEDIA_ROOT +'/car_pictures/car.png', 'rb')))
    #     car.save()

    return redirect('main')

def fixnum(request):
    # cars = Car.objects.all()
    # users = CarUser.objects.filter(is_staff=False)
    # print(len(cars))
    # print(len(users))
    # for user in users:
    #     mini_cars = cars.filter(owner=user)
    #     print(len(mini_cars))
    #     user.cars_added = len(mini_cars)
    #     user.save()
    return redirect('sellers')

def deletecar(request, pk):
    if request.user == Car.objects.get(id=pk).owner:
        if request.method == 'POST':
            Car.objects.get(id=pk).delete()
            return redirect('profile')
        return render(request, 'carseller/delete.html', {'title':Car.objects.get(id=pk).title})
    return HttpResponseForbidden()

def toggle_favorite(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)

        car_id = body_data.get('car_id')
        # Retrieve the logged-in user
        user = request.user

        # Retrieve the car object
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            print(1)
            return JsonResponse({'error': 'Car not found'}, status=404)

        # Toggle the favorite status for the user
        if car in user.fav_cars.all():
            user.fav_cars.remove(car)
            is_favorite = False
        else:
            user.fav_cars.add(car)
            is_favorite = True

        return JsonResponse({'is_favorite': is_favorite})
    
def toggle_favorite_sellers(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)

        seller_id = body_data.get('seller_id')
        # Retrieve the logged-in user
        user = request.user

        # Retrieve the car object
        try:
            seller = CarUser.objects.get(id=seller_id)
        except CarUser.DoesNotExist:
            return JsonResponse({'error': 'Seller not found'}, status=404)

        # Toggle the favorite status for the user
        if seller in user.fav_sellers.all():
            user.fav_sellers.remove(seller)
            is_favorite = False
        else:
            user.fav_sellers.add(seller)
            is_favorite = True

        return JsonResponse({'is_favorite': is_favorite})

def change_user(request):
    ctx = {}
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    name = body_data.get('full_name')
    cont = body_data.get('contacts')
    region = body_data.get('region')
    if name:
        request.user.full_name = name
    if cont:
        request.user.contacts = cont
    if region:
        request.user.region = region
        ctx = {"updt":request.user.get_region_display()}
    request.user.save()
    return JsonResponse(ctx)

