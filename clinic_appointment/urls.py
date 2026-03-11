from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', include('accounts.urls')),
    path('', include('appointments.urls')),
    path('', include('patients.urls')),
    path('', include('analytics.urls')),
]