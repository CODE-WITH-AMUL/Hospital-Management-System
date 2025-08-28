from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Patient(models.Model):
    BLOOD_GROUPS = [
        ("O+", "O+"),
        ("A+", "A+"),
        ("B+", "B+"),
        ("O-", "O-"),
        ("A-", "A-"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
    ]
    
    GENDERS = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    MARITAL_STATUS = [
        ("S", "Single"),
        ("M", "Married"),
        ("D", "Divorced"),
        ("W", "Widowed"),
    ]

    # Core Patient Info
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    username = models.CharField(max_length=250, unique=True)  # unique for login reference
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDERS)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS, blank=True, null=True)

    # Contact Info
    mobile_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()

    # Medical Info
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # e.g., 65.50 kg
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # e.g., 170.25 cm
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUPS, blank=True)
    allergies = models.TextField(blank=True, null=True, help_text="Known allergies (if any)")
    medical_history = models.TextField(blank=True, null=True, help_text="Past illnesses, chronic conditions")
    current_medications = models.TextField(blank=True, null=True)

    # Administrative Info
    appointment_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_status = models.BooleanField(default=False)

    # Relation with Doctor (optional)
    # assigned_doctor = models.ForeignKey(
    #     "Doctor", on_delete=models.SET_NULL, null=True, blank=True, related_name="patients"
    # )

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.patient_id})"
