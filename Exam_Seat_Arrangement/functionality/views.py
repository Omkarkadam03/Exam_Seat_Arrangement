from django.shortcuts import render

# Create your views here.

def autoGen(request):
    return render( request, "autoGen.html")
