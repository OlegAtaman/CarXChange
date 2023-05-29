from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='main'),
    path('profile', views.profile, name='profile'),
    path('newadd', views.NewCarAdd.as_view(), name='newadd'),
    path('seller/<int:pk>', views.sellerview, name='seller'),
    path('car/<int:pk>', views.carview, name="car"),
    path('cars', views.carlist, name='cars'),
    path('sellers', views.sellerlist, name='sellers'),
    path('filldb', views.fill_db_view)
]