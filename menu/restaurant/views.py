from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
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
    cart = request.session.get('cart', {})
    
    # Check if the item is already in the cart
    if str(item_id) in cart:
        cart[str(item_id)] += 1  # Increment quantity
    else:
        cart[str(item_id)] = 1  # Add item to cart with quantity 1
    request.session['cart'] = cart
    request.session.modified = True  # Mark the session as modified
    
    return redirect('menu')

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        del cart[str(item_id)]  # Convert item_id to string before checking
        request.session['cart'] = cart
    return redirect('cart')

@login_required
def checkout(request):
    if request.user.is_staff:
        # Redirect staff users to a different view or page
        return redirect('staff')  # Assuming 'staff_dashboard' is the URL name for the staff dashboard
    elif request.method == 'POST':
        cart = request.session.get('cart', {})
        total_price = sum(FoodItem.objects.get(id=item_id).price * quantity for item_id, quantity in cart.items())

        order = Order.objects.create(user=request.user, total_price=total_price, timestamp=timezone.now())
        for item_id, quantity in cart.items():
            food_item = FoodItem.objects.get(id=item_id)
            OrderItem.objects.create(order=order, food_item=food_item, quantity=quantity)

        del request.session['cart']
        return redirect('menu')
    else:
        return redirect('cart')
    
    