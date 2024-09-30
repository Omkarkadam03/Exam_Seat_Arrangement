from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request, "home_page.html")

def login(request):
    return render(request, "login_page.html")


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

