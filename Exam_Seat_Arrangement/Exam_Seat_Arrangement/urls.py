"""
URL configuration for Exam_Seat_Arrangement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import *
from functionality.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home_page"),
    path("login_page/", login_view, name="login_page"),
    path("Register_page/", sign_up, name="sign_up"),
    path("autoGen/", autoGen, name="autoGen"),
    path('logout/', logout_view, name='logout'),
   # path('seating_display/', seating_display, name='seating_display')

]
