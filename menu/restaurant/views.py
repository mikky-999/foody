from django.shortcuts import render, redirect
from .models import FoodItem, Order, OrderItem

def home(request):
    cart = request.session.get('cart', {})
    cart_items_count = sum(cart.values())
    return render(request, 'restaurant/home.html', {'cart_items_count': cart_items_count})

def menu(request):
    food_items= FoodItem.objects.all()
    cart = request.session.get('cart', {})
    cart_items_count = sum(cart.values())
    return render(request, 'restaurant/menu.html', {'food_items':food_items, 'cart_items_count': cart_items_count})

def cart(request):
    cart = request.session.get('cart', {})
    cart_items_count = sum(cart.values())
    total_price = 0
    items = []
    for item_id, quantity in cart.items():
        food_item = FoodItem.objects.get(id=item_id)
        total_price += food_item.price * quantity
        items.append({'food_item': food_item, 'quantity': quantity})
    return render(request, 'restaurant/cart.html', {'items': items, 'total_price': total_price, 'cart_items_count': cart_items_count})
    

def add_to_cart(request, item_id):
    if 'cart' not in request.session:
        request.session['cart']= {}

    cart = request.session['cart']
    cart[item_id] = cart.get(item_id, 0) + 1
    request.session.modified = True  
    return redirect('menu')