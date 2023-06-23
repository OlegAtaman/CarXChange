from django.urls import path, include
from rest_framework.authtoken import views as rest_views

from carseller.api import views


urlpatterns = [
    path('', views.preview, name='api_preview'),
    path('cars/', views.car_list, name='carlist_api'),
    path('users/', views.user_list, name='userlist_api'),
    path('car/<car_id>/', views.car_detail, name='cardetail_api'),
    path('user/<user_id>/', views.user_detail, name='userdetail_api'),
    # Auth
    path("auth/", include("rest_framework.urls")),
    path("token-auth/", rest_views.obtain_auth_token)
]