from django.urls import path
from .views import *


urlpatterns = [
    path('' , doctor_dashboard , name='doctor_dashboard'),
    path('doctor/profile' , doctor_profile , name='doctor_profile')
]
