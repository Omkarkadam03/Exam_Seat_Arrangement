from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

# Create your views here.
def home(request):
    return render(request, "home_page.html")

# home/views.py
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Log in the user
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('autoGen')  # Redirect to home page after successful login
        else:
            # If authentication fails
            messages.error(request, "Invalid email or password.")
            return redirect('login_page')
    
    return render(request, 'Login_page.html')



def sign_up(request):
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('sign_up')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('sign_up')

        user = User.objects.create_user(username=email, email=email, password=password1)
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect("autoGen")  # Redirect to home page after signup

    return render(request, "SignUp_page.html")

def logout_view(request):
    logout(request)
    return redirect('home_page')

