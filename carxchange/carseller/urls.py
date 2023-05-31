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
    path('deletecar/<int:pk>', views.deletecar, name='delete'),
    path('toggle_favorite', views.toggle_favorite, name='toggle_favorite'),
    path('toggle_favorite_sellers', views.toggle_favorite_sellers, name='toggle_favorite_sellers'),
    path('changeuser', views.change_user, name="change_user"),
    path('filldb', views.fill_db_view),
    path('fixnum', views.fixnum)
]