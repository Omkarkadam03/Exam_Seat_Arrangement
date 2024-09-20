from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request, "home_page.html")

def login(request):
    return render(request, "login_page.html")

def sign_up(request):
    return render(request, "SignUp_page.html")
