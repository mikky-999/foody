from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse_lazy
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from PIL import Image
from .mixin import LoginRequiredMixin, StaffRequiredMixin, UserRequiredMixin, non_staff_required
from restaurant.models import Order, User, FoodItem
from .forms import CustomerRegister

def register(request):
    if request.method == 'POST':
        form = CustomerRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            print(f"{username} created successfully")
            messages.success(request, f'Account created for {username}!')
        return redirect('login')
    else:
        form = CustomerRegister()
    return render(request, 'users/register.html', {'form': form})    

def logout_view(request):
     logout(request)
     messages.success(request, f'You logged out!')
     return redirect('restaurant-home')

# Some decorators
@staff_member_required
@login_required
def change_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = 'DELIVERED'
    order.save()
    return redirect ('staff-order')

# some decorators
@staff_member_required
@login_required
def out_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        order.status = 'OUT OF STOCK'
        order.save()
        return redirect ('staff-order')
    return redirect('staff')       

@non_staff_required
@login_required
def delete_order(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(pk=order_id)
        order.delete()
        return redirect('profile-order')

#staff restriction to be applied
@staff_member_required
@login_required    
def delete_food(request, FoodItem_id):
    food_item = get_object_or_404(FoodItem, pk=FoodItem_id)
    if request.method == 'POST':
        food_item.delete()
        return redirect('staff-menu')    

class ProfileAccountView(LoginRequiredMixin, UserRequiredMixin, ListView):
    model= User
    template_name= 'users/profile/account.html'

class UserUpdateView(LoginRequiredMixin, UserRequiredMixin, UpdateView):
    model= User
    fields=['username', 'email']
    template_name= 'users/profile/foodupdate.html' 
    success_url = reverse_lazy('profile-account')   

class UserOrderView(LoginRequiredMixin, UserRequiredMixin, ListView):
    model= Order
    template_name= 'users/profile/stafforders.html'
    context_object_name= 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class HistoryTabView(LoginRequiredMixin, UserRequiredMixin, ListView):
    model = Order
    template_name ='users/profile/food.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='DELIVERED')
   

class AccountView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model= User
    template_name= 'users/staff/account.html'

class FoodUpdateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model= FoodItem
    fields= ['name', 'description', 'price', 'image']
    template_name= 'users/staff/foodupdate.html'
    success_url = reverse_lazy('foodupdate')
    
    def form_valid(self, form):
        # Resize the image
        image_field = form.cleaned_data['image']
        image = Image.open(image_field)
        resized_image = image.resize((300, 300))

        # Generate a unique name for the resized image
        image_name = f"{image_field.name.split('.')[0]}_resized.jpg"

        # Save the resized image back to the form's cleaned data
        output = BytesIO()
        resized_image.save(output, format='JPEG', quality=100)
        output.seek(0)
        form.cleaned_data['image'] = InMemoryUploadedFile(output, 'ImageField', image_name, 'image/jpeg', output.getbuffer().nbytes, None)

        return super().form_valid(form)


class DisplayMenuView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model= FoodItem
    template_name= 'users/staff/food.html'
    context_object_name= 'food_items'

class DisplayOrderView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model= Order
    template_name= 'users/staff/stafforders.html'
    context_object_name= 'orders'

    def get_queryset(self):
        return Order.objects.select_related('user').prefetch_related('food_items').all().annotate(total_quantity=Sum('food_items__quantity'))
    
