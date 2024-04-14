from django.shortcuts import render



def home(request):
    return render(request, "all/home.html",{})

def company_login(request):
    return render(request, "all/login-company.html",{})

def emp_login(request):
    return render(request, "all/login-employee.html",{})

def cus_login(request):
    return render(request, "all/login-customer.html",{})

def company_signup(request):
    return render(request, "all/signup-company.html",{})

def cus_signup(request):
    return render(request, "all/signup-customer.html",{})