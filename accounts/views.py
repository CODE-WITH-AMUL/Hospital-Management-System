from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout as user_logout


MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.SUCCESS: 'success',
}

# =========================
# Customer Login
# =========================
def costumer_login(request):
    if request.method == "POST":
        number = request.POST.get('number')  # Use phone number instead of username
        password = request.POST.get('password')

        user = authenticate(request, username=number, password=password)  # username stores number
        if user:
            user_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('reception')
        else:
            messages.error(request, "Invalid number or password")
            return redirect('costumer_login')

    return render(request, 'costumer_login.html')


# =========================
# Customer Registration
# =========================
def costumer_register(request):
    if request.method == "POST":
        number = request.POST.get('number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('costumer_register')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect('costumer_register')

        # Check if number already exists
        if User.objects.filter(username=number).exists():
            messages.error(request, "Number already registered")
            return redirect('costumer_register')

        # Create new user
        user = User.objects.create_user(username=number, password=password)
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('costumer_login')

    return render(request, 'costumer_register.html')


# =========================
# Customer Logout
# =========================
def costumer_logout(request):
    user_logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('costumer_login')
