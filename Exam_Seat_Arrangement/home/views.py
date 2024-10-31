from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetView

# Create your views here.
def home(request):
    return render(request, "home_page.html")

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        remember = request.POST.get('remember', False)
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            
            # If "Remember Me" is not checked, set session expiry to browser close
            if not remember:
                request.session.set_expiry(0)  # Expires on browser close
            else:
                request.session.set_expiry(1209600)  # 2 weeks
            
            messages.success(request, "Login successful!")
            return redirect('autoGen')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login_page')
    
    return render(request, 'Login_page.html')





# Signup view
def sign_up(request):
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validate passwords
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('sign_up')

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('sign_up')

        # Create new user
        user = User.objects.create_user(username=email, email=email, password=password1)
        user.save()

        # Authenticate and log the user in immediately
        user = authenticate(request, username=email, password=password1)
        if user is not None:
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('autoGen')  # Redirect to home page after signup

    return render(request, "SignUp_page.html")

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home_page')


def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Process the contact form submission (e.g., save to database, send email notification)
        # Here, we will just display a success message
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact_page')
    return render(request,'contact_page.html')
