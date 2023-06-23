from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.shortcuts import render

from carseller.models import Car
from .serializers import CarSerializer, UserSerializer


user_model = get_user_model()

def preview(request):
    return render(request, 'api/preview.html')


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def car_list(request):

    if request.method == 'GET':
        if request.GET.get('fav') and request.user.is_authenticated:
            cars = request.user.fav_cars.all()
        else:
            cars = Car.objects.all()
        serialized = CarSerializer(cars, many=True, context={'request': request})
        return Response({'data': serialized.data})
    
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'Error':'You must be authenticated!'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        data.update({'owner':request.user.id})
        serializer = CarSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_list(request):
    if request.GET.get('fav') and request.user.is_authenticated:
        users = request.user.fav_sellers.all()
    else:
        users = user_model.objects.filter(is_staff=False)
    serialized = UserSerializer(users, many=True, context={'request': request})
    return Response({'data': serialized.data})


@api_view(['GET', 'DELETE'])
def car_detail(request, car_id):

    try:
        car = Car.objects.get(id=car_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serialized = CarSerializer(car, context={'request': request})
        return Response({'data': serialized.data})
    
    if request.method == 'DELETE':
        if car.owner == request.user:
            car.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'Error':'Thats not your car!'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'PUT'])
@parser_classes([MultiPartParser, FormParser])
def user_detail(request, user_id):

    try:
        user = user_model.objects.get(id=user_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serialized = UserSerializer(user, context={'request': request})
        return Response({'data': serialized.data})
    
    if request.method == 'PUT':
        if request.user.is_authenticated:
            if request.user != user:
                return Response({'Error':'Thats not your account!'}, status=status.HTTP_403_FORBIDDEN)
        serialized = UserSerializer(user, data=request.data, partial=True)
        
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
