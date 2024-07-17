from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

@login_required
def profile(request):
    return render(request, 'users/profile.html')


# Create your views here.
