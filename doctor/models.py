from django.db import models

class Doctor(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    doctor_id = models.AutoField(primary_key=True)
    doctor_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    license_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    hospital = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    availability_days = models.CharField(max_length=200, blank=True, null=True)  # e.g., "Mon-Fri"
    availability_time = models.CharField(max_length=100, blank=True, null=True) # e.g., "10:00AM - 5:00PM"
    profile_picture = models.ImageField(upload_to='doctor_profiles/', null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    reviews_count = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    profile_created_at = models.DateTimeField(auto_now_add=True)
    profile_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.doctor_name} ({self.specialization})"
