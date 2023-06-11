from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponseForbidden, JsonResponse
import json


from .filter import filter
from .models import Car
from .forms import CarForm
import carseller.choices as ch
from users.choices import REGION_CHOICES
from users.models import CarUser


def index(request):
    return render(request, 'carseller/index.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
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
        if not request.user.is_authenticated:
            return redirect('login')
        ctx = {
            'form':CarForm()
        }
        return render(request, self.template, ctx)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
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
    if request.GET.get('fav') and request.user.is_authenticated:
        cars = request.user.fav_cars.all()
        favsearch = True
    cars = filter(cars, request.GET)
    pages = len(cars)//10+1
    cars = cars[10*(page-1):10*page]
    favs = []
    if request.user.is_authenticated:
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
    if request.GET.get('fav') and request.user.is_authenticated:
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
    if request.user.is_authenticated:
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

def changeave(request):
    # body_unicode = request.body.decode('utf-8')
    # body_data = json.loads(body_unicode)
    image = request.FILES['image']
    user = request.user
    user.picture = image
    user.save()
    ctx = {'utd_img':user.picture.url}
    return JsonResponse(ctx)