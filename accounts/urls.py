from django.urls import path
from . import views

urlpatterns = [
    path('Cotumer/login/', views.costumer_login, name='costumer_login'),
    path('Costmer/register/', views.costumer_register, name='costumer_register'),
    path('Costumer/logout/', views.costumer_logout, name='costumer_logout'),

]