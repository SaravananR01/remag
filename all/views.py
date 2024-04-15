from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.hashers import check_password,make_password
import random,bcrypt


def gen_id():
    chars=[chr(x) for x in range (65,91)]
    nums=[chr(x) for x in range (48,58)]
    return random.choice(chars)+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)

def check_password(password,hashed_password):
    
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def home(request):
    return render(request, "all/home.html",{})

def company_login(request):
    context={}
    if request.method == "POST":
        c_email=request.POST['email']
        c_password = str(request.POST['password'])
        
        users = Company.objects.filter(c_email=c_email)
        if len(users)<1:
            context['error']="No company with this email found. Please create a new account."
        else:
            print(check_password(c_password,users[0].c_password))
            if check_password(c_password, users[0].c_password):
                request.session['company']=c_email
                request.session['loggedin']=True
                request.session.modified=True
                request.session.set_expiry(600)
                return redirect("/companypage")
            else:
                context['error']="Invalid Password. Please try again."

    return render(request, "all/login-company.html",context=context)

def emp_login(request):
    return render(request, "all/login-employee.html",{})

def cus_login(request):
    return render(request, "all/login-customer.html",{})

def company_signup(request):
    context={}
    if request.method == 'POST':
        c_name = request.POST['company-name']
        c_phone = request.POST['company-phone']
        c_addr = request.POST['inputAddress']+" "+request.POST['inputAddress2']
        c_email = request.POST['company-email']
        password = request.POST['company-pwd']
        cnfpass = request.POST['cnf-pwd']

        if password!=cnfpass:
            context['error']="PASSWORDS DO NOT MATCH!"
        else:
            users = Company.objects.filter(c_email=c_email)
            if len(users)>0:
                print(users)
                context['error']="Company already exists. Please log-in."
            elif c_name=="" or c_phone=="" or (not c_phone.isdigit()) or (len(c_phone)!=10) or c_addr==" " or c_email=="" or password=="":
                context['error']="Blank Fields are not allowed."
            else:
                new_comp=Company.objects.create(
                    c_id=gen_id(),
                    c_name=c_name,
                    c_phone=c_phone,
                    c_address=c_addr,
                    c_email=c_email,
                    c_password=password
                )
                return redirect("/logincompany")
        

    return render(request, "all/signup-company.html",context=context)

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

    return render(request,"all/edit-branch.html",{})
