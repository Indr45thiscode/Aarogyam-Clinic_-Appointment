from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.public_home, name='public_home'),
    path('book-appointment/', views.public_home, name='book_appointment'),
    path('api/available-slots/', views.get_available_slots, name='available_slots'),

    # Doctors
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/add/', views.doctor_add, name='doctor_add'),
    path('doctors/<int:pk>/edit/', views.doctor_edit, name='doctor_edit'),
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),

    # Appointments
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/add/', views.appointment_add, name='appointment_add'),
    path('appointments/<int:pk>/status/', views.appointment_update_status, name='appointment_update_status'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),

    # Prescription
    path('appointments/<int:appointment_id>/prescription/add/', views.add_prescription, name='add_prescription'),
    path('appointments/<int:appointment_id>/prescription/',      views.view_prescription, name='view_prescription'),
    path('appointments/<int:appointment_id>/prescription/pdf/',  views.prescription_pdf, name='prescription_pdf'),
]