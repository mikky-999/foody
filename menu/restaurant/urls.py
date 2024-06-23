from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='restaurant-home'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]