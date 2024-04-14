from django.shortcuts import render



def home(request):
    return render(request, "all/home.html",{})
