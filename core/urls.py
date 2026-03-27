from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from farms import views as farm_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('farms.urls')), 
    
    # Auth System
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', farm_views.register, name='register'), # This now finds the function!
]