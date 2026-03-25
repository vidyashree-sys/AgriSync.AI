from django.contrib import admin
from django.urls import path, include
from farms import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('', views.dashboard, name='dashboard'),
    # This line MUST have name='predict_crop'
    path('predict/<int:farm_id>/', views.predict_crop, name='predict_crop'),
]