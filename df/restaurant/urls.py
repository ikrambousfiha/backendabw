from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact_form, name='contact_form'),
    path('reservation/', views.reservation_form, name='reservation_form'),
]