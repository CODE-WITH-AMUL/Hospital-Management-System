from django.shortcuts import render
from doctor.models import Doctor


def create_doctor(request):
    if request.method == "POST":
        doctor = Doctor(
            doctor_name=request.POST['name'],
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        
        doctor.set_password(request.POST['password'])
        doctor.save()