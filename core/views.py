import os
import json
import uuid
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

# File path for storing patient and doctor data
PATIENT_FILE = os.path.join(settings.BASE_DIR, 'patients.json')
DOCTOR_FILE = os.path.join(settings.BASE_DIR, 'information/doctors.json')


def index(request):
    return render(request, 'index.html')


def reception(request):
    # Load patients from JSON file
    if os.path.exists(PATIENT_FILE):
        try:
            with open(PATIENT_FILE, 'r') as f:
                patients = json.load(f)
        except json.JSONDecodeError:
            patients = []
    else:
        patients = []

    search_query = request.GET.get('search_query', '').strip().lower()
    
    if search_query:
        patients = [
            p for p in patients
            if search_query in p.get('firstname', '').lower()
            or search_query in p.get('lastname', '').lower()
            or search_query in p.get('username', '').lower()
            or search_query in (p.get('firstname', '') + " " + p.get('lastname', '')).lower()
        ]

    if request.method == 'POST':
        patient = {
            'patient_id': str(uuid.uuid4())[:8],  # unique ID
            'firstname': request.POST.get('firstname'),
            'lastname': request.POST.get('lastname'),
            'username': request.POST.get('username'),
            'dob': request.POST.get('dob'),  # date of birth
            'age': request.POST.get('age'),
            'gender': request.POST.get('gender'),
            'blood_group': request.POST.get('blood_group'),
            'weight': request.POST.get('weight'),
            'mobile_number': request.POST.get('mobile_number'),
            'email': request.POST.get('email'),
            'address': request.POST.get('address'),
            'marital_status': request.POST.get('marital_status'),
            'occupation': request.POST.get('occupation'),
            'nationality': request.POST.get('nationality'),
            'emergency_contact_name': request.POST.get('emergency_contact_name'),
            'emergency_contact_number': request.POST.get('emergency_contact_number'),
            'reason_for_visit': request.POST.get('reason_for_visit'),
            'medical_history': request.POST.get('medical_history'),
            'insurance_provider': request.POST.get('insurance_provider'),
            'insurance_policy_number': request.POST.get('insurance_policy_number'),
            'admission_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'payment_status': True if request.POST.get('payment_status') == 'on' else False,
        }

        patients.append(patient)
        with open(PATIENT_FILE, 'w') as f:
            json.dump(patients, f, indent=4)

        return redirect('reception')

    return render(request, 'reception.html', {
        'patients': patients,
        'query': search_query
    })


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


def doctor_profile(request):
    # This view seems to be based on Django's ORM, while others use JSON files.
    # We will assume this is separate for now.
    from .models import Doctor
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


def patient_details(request, patient_id):
    """
    Handles displaying a single patient's details and appointments.
    """
    # Load all patients to find the one with the matching ID
    patients = []
    if os.path.exists(PATIENT_FILE):
        try:
            with open(PATIENT_FILE, 'r') as f:
                patients = json.load(f)
        except json.JSONDecodeError:
            pass

    # Find the specific patient by patient_id
    patient = next((p for p in patients if p.get('patient_id') == patient_id), None)
    
    if not patient:
        raise Http404("Patient not found")

    # This is placeholder data for appointments. In a real app,
    # you would fetch this from a database.
    appointments = [
        {
            'date': '2024-05-20',
            'time': '10:00 AM',
            'doctor': 'Dr. Alan Grant',
            'reason': 'Routine check-up',
            'status': 'Successful',
        },
        {
            'date': '2024-06-15',
            'time': '02:30 PM',
            'doctor': 'Dr. Ellie Sattler',
            'reason': 'Follow-up on allergy test',
            'status': 'Pending',
        },
    ]

    return render(request, 'patient_details.html', {
        'patient': patient,
        'appointments': appointments,
    })

