import os
import json
from datetime import datetime
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from .models import Doctor


# File path for storing patient and doctor data
PATIENT_FILE = os.path.join(settings.BASE_DIR, 'patients.json')
DOCTOR_FILE = os.path.join(settings.BASE_DIR, 'information/doctors.json')


'''
Doctor Dashboard:
- Loads doctors from JSON
- Allows searching doctors
- Loads patients from JSON
- Allows searching patients
'''
def doctor_dashboard(request):
    # Load doctors from JSON
    if os.path.exists(DOCTOR_FILE):
        try:
            with open(DOCTOR_FILE, 'r') as f:
                doctors = json.load(f)
        except json.JSONDecodeError:
            doctors = []
    else:
        doctors = []

    # Doctor search query
    doctor_query = request.GET.get('doctor_search', '').strip().lower()
    if doctor_query:
        doctors = [
            doctor for doctor in doctors
            if doctor_query in doctor.get('name', '').lower()
            or doctor_query in doctor.get('email', '').lower()
            or doctor_query in doctor.get('phone', '').lower()
        ]

    # Load patients from JSON
    if os.path.exists(PATIENT_FILE):
        try:
            with open(PATIENT_FILE, 'r') as f:
                patients = json.load(f)
        except json.JSONDecodeError:
            patients = []
    else:
        patients = []

    # Patient search query
    patient_query = request.GET.get('patient_search', '').strip().lower()
    if patient_query:
        patients = [
            p for p in patients
            if patient_query in p.get('firstname', '').lower()
            or patient_query in p.get('lastname', '').lower()
            or patient_query in p.get('username', '').lower()
            or patient_query in (p.get('firstname', '') + " " + p.get('lastname', '')).lower()
        ]

    return render(request, 'doctor_dashboard.html', {
        "doctors": doctors,
        "patients": patients,
    })


'''
Doctor Profile:
- Fetches doctor by ID from session
- Updates profile if POST
- Returns updated doctor in context
'''
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import Doctor

def doctor_profile(request):
    doctor_id = request.session.get('doctor_id')
    doctor = get_object_or_404(Doctor, pk=doctor_id)

    if request.method == "POST":
        # Basic Info
        doctor.doctor_name = request.POST.get('name')
        doctor.username = request.POST.get('username')
        doctor.email = request.POST.get('email')
        doctor.phone = request.POST.get('phone')
        doctor.dob = request.POST.get('DOB')
        doctor.gender = request.POST.get('gender')
        doctor.address = request.POST.get('address')

        # Professional Info
        doctor.specialization = request.POST.get('specialization')
        doctor.qualification = request.POST.get('qualification')
        doctor.experience_years = request.POST.get('experience_years') or 0
        doctor.license_number = request.POST.get('license_number')
        doctor.hospital = request.POST.get('hospital')
        doctor.department = request.POST.get('department')

        # Availability & Work
        doctor.consultation_fee = request.POST.get('consultation_fee') or 0.00
        doctor.availability_days = request.POST.get('availability_days')
        doctor.availability_time = request.POST.get('availability_time')

        # File upload (optional)
        if 'profile_picture' in request.FILES:
            doctor.profile_picture = request.FILES['profile_picture']

        doctor.profile_updated_at = datetime.now()
        doctor.save()

        return redirect('doctor_profile')  # Refresh after update

    context = {
        "doctor": doctor
    }
    return render(request, 'doctor_profile.html', context)
