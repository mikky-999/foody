"""
URL configuration for menu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as users_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('new_me/', admin.site.urls),
    path('', include('restaurant.urls')),
    path('register/', users_views.register, name='register'),
    path('profile/order/delete/<int:order_id>/', users_views.delete_order, name='delete-order'),
    path('staff/food/delete/<int:FoodItem_id>/', users_views.delete_food, name='delete-food'),
    path('profile/account', users_views.ProfileAccountView.as_view(), name='profile-account'),
    path('profile/update/<int:pk>/now/', users_views.UserUpdateView.as_view(), name='profile-update'),
    path('profile/order', users_views.UserOrderView.as_view(), name='profile-order'),
    path('profile/history', users_views.HistoryTabView.as_view(), name='profile-history'),
    path('staff/order/change/<int:order_id>/', users_views.change_order_status, name='change-status'),
    path('staff/order/out/<int:order_id>/', users_views.out_order_status, name='out-status'),
    path('staff/account', users_views.AccountView.as_view(), name='staff-account'),
    path('staff/update', users_views.FoodUpdateView.as_view(), name='foodupdate'),
    path('staff/food', users_views.DisplayMenuView.as_view(), name='staff-menu'),
    path('staff/order', users_views.DisplayOrderView.as_view(), name='staff-order'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', users_views.logout_view, name='logout'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
