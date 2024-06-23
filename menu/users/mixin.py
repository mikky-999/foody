from django.shortcuts import redirect
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.urls import reverse_lazy
from restaurant.models import Order

class UserRequiredMixin(UserPassesTestMixin):
    login_url = reverse_lazy('login')  # URL name of your login view

    def test_func(self):
        return not self.request.user.is_staff

    def handle_no_permission(self):
        return redirect(self.login_url)
    
class StaffRequiredMixin(UserPassesTestMixin):
    login_url = reverse_lazy('login')  # URL name of your login view

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect(self.login_url)    

def user_is_not_staff(user):
    return not user.is_staff

def non_staff_required(view_func=None, redirect_field_name='next', login_url='login'):
    actual_decorator = user_passes_test(
        user_is_not_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

""" class DeleteOrder(LoginRequiredMixin, UserRequiredMixin, DeleteView):
    model = Order
    success_url = '/ '

    def test_func(self):
        order_id = self.kwargs.get('order_id')  # Assuming you're using order_id in URL kwargs
        if order_id:
            order = Order.objects.get(id=order_id)
            return self.request.user == order.user
        else:
            raise Http404("Order ID not found") """