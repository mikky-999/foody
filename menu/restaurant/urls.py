from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='restaurant-home'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
]