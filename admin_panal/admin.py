from django.contrib import admin
from core.models import Patient
from doctor.models import Doctor

# Registering Patient using the decorator is also a good practice
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'patient_id',
        'first_name',
        'last_name',
        'username',
        'date_of_birth',
        'age',
        'gender',
        'marital_status',
        'mobile_number',
        'email',
        'address',
        'weight',
        'height',
        'blood_group',
        'allergies',
        'medical_history',
        'current_medications',
        'appointment_date',
        'created_at',
        'updated_at',
        'payment_status',
    )



@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'doctor_id',
        'doctor_name',
        'username',
        'email',
        'phone',
        'dob',
        'gender',
        'address',
        'specialization',
        'qualification',
        'experience_years',
        'license_number',
        'hospital',
        'department',
        'consultation_fee',
        'availability_days',
        'availability_time',
        'rating',
        'reviews_count',
        'status',
        'profile_created_at',
        'profile_updated_at',
    )