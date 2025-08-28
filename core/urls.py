from django.urls import path
from .views import index, reception, patient_details

urlpatterns = [
    path('', index, name='index'),
    path('details/', reception, name='reception'),
    path('patient/<str:patient_id>/',patient_details, name='patient_details'),
]
