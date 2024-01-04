from .models import Car
from random import randrange


def get_three_cars(car):
    # print(car)
    brand = car.brand
    all_cars = list(Car.objects.exclude(id=car.id))
    same_brand_cars_qs = list(Car.objects.filter(brand=brand))
    same_brand_cars = []
    for iter_car in same_brand_cars_qs:
        if iter_car != car:
            same_brand_cars.append(iter_car)
    out_car_list = []
    while len(out_car_list) < 3:
        # print(same_brand_cars)
        # print(all_cars)
        # print(out_car_list)
        if len(same_brand_cars) > 0:
            out_car_list.append(same_brand_cars.pop(randrange(len(same_brand_cars))))
        else:
            car = all_cars.pop(randrange(len(all_cars)))
            if car not in out_car_list:
                out_car_list.append(car)
    # print(out_car_list)
    return out_car_list


def generate_string():
    string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    out = ""
    for i in range(15):
        out += string[randrange(len(string))]
    return out