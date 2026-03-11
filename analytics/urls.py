from django.urls import path
from . import views

urlpatterns = [
    path('analytics/', views.analytics, name='analytics'),
    path('reports/', views.reports, name='reports'),
]