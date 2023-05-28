from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model

from .models import Car
from .forms import CarForm
import carseller.choices as ch


def index(request):
    return render(request, 'carseller/index.html')

def profile(request):
    user = request.user
    cars = Car.objects.filter(owner=user)
    count = len(cars)
    ctx = {
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
    cars = Car.objects.all()
    ctx = {
        'cars': cars,
        'fuel_choices': ch.FUEL_CHOICES,
        'accident_choices': ch.ACCIDENTS_CHOICES,
        'trans_choices': ch.TRANS_CHOICES,
        'brand_choices': ch.BRAND_CHOICES,
        'wheel_choices': ch.WHEEL_CHOICES
    }
    return render(request, 'carseller/cars.html', ctx)

def sellerlist(request):
    user_model = get_user_model()
    sellers = user_model.objects.all()
    return render(request, 'carseller/sellers.html', {'sellers':sellers})