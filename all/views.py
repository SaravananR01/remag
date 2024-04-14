from django.shortcuts import render,redirect
from .models import *

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

def company_page(request):
    return render(request,"all/company-page.html",{})

def branch_page(request):
    return render(request,"all/edit-branch.html",{})

def edit_emp(request):
    return render(request,"all/edit-employee.html",{})

def edit_shop(request):
    return render(request,"all/edit-shop.html",{})

def edit_warehouse(request):
    return render(request,"all/edit-warehouse.html",{})

def emp_page(request):
    return render(request,"all/employee-page.html",{})

def modify_item_details(request):
    return render(request,"all/modify_tem_details.html",{})

def modify_stock(request):
    return render(request,"all/modify_stock.html",{})

def transaction_details(request):
    return render(request,"all/transaction_details.html",{})

def transaction(request):
    return render(request,"all/transaction.html",{})

def add_item(request):
    return render(request,"all/add_itm.html",{})

def source_items(request):
    return render(request,"all/source_items.html",{})

def customerpage(request):
    return render(request,"all/customer-page.html",{})

def changeshop(request):
    if request.method == 'POST':
        s_id = request.POST.get('id')
        b_id = request.POST.get('b_id')
        s_admin_id = request.POST.get('admin_id')

        branch = Branch.objects.get(pk=b_id)

        store = Store.objects.create(s_id=s_id, b_id=branch, s_admin_id=s_admin_id)
    return redirect('/companypage')

def changewarehouse(request):
    if request.method == 'POST':
        w_id = request.POST.get('id')
        b_id = request.POST.get('b_id')
        w_admin_id = request.POST.get('admin_id')

        branch = Branch.objects.get(pk=b_id)

        warehouse = Warehouse.objects.create(w_id=w_id, b_id=branch, w_admin_id=w_admin_id)
    return redirect('/companypage')

