from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth.password_validation import validate_password
import random,bcrypt,datetime


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
            if check_password(c_password, users[0].c_password):
                request.session['company']=users[0].c_id
                request.session.pop('emp',None)
                request.session.pop('cus',None)
                request.session['email']=users[0].c_email
                request.session.modified=True
                request.session.set_expiry(600)
                return redirect("/companypage")
            else:
                context['error']="Invalid Password. Please try again."

    return render(request, "all/login-company.html",context=context)

def emp_login(request):
    context={}
    if request.method == "POST":
        emp_email=request.POST['email']
        emp_password = str(request.POST['password'])
        
        users = Employee.objects.filter(emp_email=emp_email)
        if len(users)<1:
            context['error']="No employee with this email found. Please create the employee account in the company page first."
        else:
            if check_password(emp_password, users[0].emp_password):
                request.session['emp']=users[0].emp_id
                request.session.pop('company',None)
                request.session.pop('cus',None)
                request.session['email']=users[0].emp_email
                request.session.modified=True
                request.session.set_expiry(600)
                return redirect("/emp-page")
            else:
                context['error']="Invalid Password. Please try again."

    return render(request, "all/login-employee.html",context)

def cus_login(request):
    context={}
    if request.method == "POST":
        cus_email=request.POST['email']
        cus_password = str(request.POST['password'])
        
        users = Customers.objects.filter(cus_email=cus_email)
        if len(users)<1:
            context['error']="No customer with this email found. Please create a new account."
        else:
            if check_password(cus_password, users[0].cus_password):
                request.session['cus']=users[0].cus_id
                request.session.pop('emp',None)
                request.session.pop('company',None)
                request.session['email']=users[0].cus_email
                request.session.modified=True
                request.session.set_expiry(600)
                return redirect("/customer")
            else:
                context['error']="Invalid Password. Please try again."
    return render(request, "all/login-customer.html",context=context)

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
                context['error']="Company already exists. Please log-in."
            elif c_name=="" or c_phone==""  or c_addr==" " or c_email=="" or password=="":
                context['error']="Blank Fields are not allowed."
            elif (not c_phone.isdigit()) or (len(c_phone)!=10):
                context['error']="Invalid phone number."
            else:
                try:
                    validate_password(password)
                except Exception as e:
                    context['error']="Please use a stronger password. "+" ".join(e)
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
    context={}
    if request.method == 'POST':
        cus_name = request.POST['customer-name']
        cus_phone = request.POST['customer-phone']
        cus_dob = request.POST['customer-dob']
        cus_email = request.POST['customer-email']
        password = request.POST['customer-pwd']
        cnfpass = request.POST['customer-pwd2']
        if cus_dob!="":
            cus_dob = datetime.datetime.strptime(cus_dob, '%Y-%m-%d').date()
        if password!=cnfpass:
            context['error']="PASSWORDS DO NOT MATCH!"
        else:
            users = Customers.objects.filter(cus_email=cus_email)
            if len(users)>0:
                context['error']="Customer already exists. Please log-in."
            elif cus_name=="" or cus_phone==""  or cus_dob=="" or cus_email=="" or password=="":
                context['error']="Blank Fields are not allowed."
            elif cus_dob.year>datetime.date.today().year or cus_dob.year<datetime.date.today().year-100:
                context['error']="Invalid date of birth."
            elif (not cus_phone.isdigit()) or (len(cus_phone)!=10):
                context['error']="Invalid phone number."
            else:
                
                try:
                    validate_password(password)
                except Exception as e:
                    context['error']="Please use a stronger password. "+" ".join(e)
                else:
                    new_comp=Customers.objects.create(
                        cus_id=gen_id(),
                        cus_name=cus_name,
                        cus_join_date=datetime.date.today(),
                        cus_points=0,
                        dob= cus_dob,
                        cus_phone_no=cus_phone,
                        cus_email=cus_email,
                        cus_password=password
                    )
                    return redirect("/logincus")
        
    return render(request, "all/signup-customer.html",context)

def company_page(request):
    context={}
    if 'company' in request.session:
        user = Company.objects.filter(c_id=request.session['company'])
        if len(user)>0:
            context['email']=request.session['email']
            return render(request,"all/company-page.html",context=context)
    return redirect("/logincompany")

def branch_page(request):
    return render(request,"all/edit-branch.html",{})

def edit_emp(request):
    return render(request,"all/edit-employee.html",{})

def edit_shop(request):
    return render(request,"all/edit-shop.html",{})

def edit_warehouse(request):
    return render(request,"all/edit-warehouse.html",{})

def emp_page(request):
    context={}
    if 'emp' in request.session:
        user = Employee.objects.filter(emp_id=request.session['emp'])
        if len(user)>0:
            context['email']=request.session['email']
            #logic
            return render(request,"all/employee-page.html",context=context)
    return redirect("/loginemp")
    

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
    context={}
    if 'cus' in request.session:
        user = Customers.objects.filter(cus_id=request.session['cus'])
        if len(user)>0:
            context['email']=request.session['email']
            return render(request,"all/customer-page.html",context=context)
    return redirect("/cuslogin")
    

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

def logout(request):
    request.session.clear()
    request.session.flush()
    return redirect('/')