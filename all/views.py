from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.hashers import check_password,make_password
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.password_validation import validate_password
import random,bcrypt,datetime,time


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
    context = {}
    if 'company' in request.session:
        user = Company.objects.filter(c_id=request.session['company'])
        company=Company.objects.get(pk=request.session['company'])
        if user.exists():
            context['company_id'] = company.c_id
            context['company_name'] = company.c_name
            context['email'] = request.session['email']
            company_branches = Branch.objects.filter(company=request.session['company'])
            all_stores = []
            all_warehouses = []

            for branch in company_branches:
                stores = Store.objects.filter(branch=branch)
                warehouses = Warehouse.objects.filter(branch=branch)
                all_stores.extend(stores)
                all_warehouses.extend(warehouses)
            context['all_stores'] = all_stores
            context['all_warehouses'] = all_warehouses
            return render(request, "all/company-page.html", context=context)

    return redirect("/logincompany")

def add_branch(request):
    context = {}
    if 'company' in request.session:
        user = Company.objects.filter(c_id=request.session['company'])
        company=Company.objects.get(pk=request.session['company'])
        if user.exists():
            b_id=gen_id()
            context['branch_id']=b_id
            context['company_id']=company.c_id
            if request.method == 'POST':
                b_address=request.POST.get('address')
                b_phone_no=request.POST.get('phone-no')
                new_branch=Branch.objects.create(
                    b_id=b_id,
                    company=company,
                    b_address=b_address,
                    b_phone_no=b_phone_no
                )
                new_branch.save()
                return redirect("/companypage")
            return render(request, "all/add-branch.html", context=context)
    return redirect("/logincompany")

def branch_page(request):
    all_emps=Employee.objects.all() 
    url=reverse("edit")
    return render(request,"all/edit-branch.html",{'all_emps':all_emps,'url':url})


def add_emp(request):
    context = {}
    if 'company' in request.session:
        user = Company.objects.filter(c_id=request.session['company'])
        company_branches = Branch.objects.filter(company=request.session['company'])
        all_branches=[]
        for branch in company_branches:
            all_branches.append(branch.b_id)
        context['company_branches']=all_branches
        if user.exists():
                emp_id=gen_id()
                context['emp_id']=emp_id
                if request.method == 'POST':
                    branch_id=request.POST.get('branch')
                    branch_id = branch_id[branch_id.find("(")+1:branch_id.find(")")]
                    branch=Branch.objects.get(b_id=branch_id)
                    ename = request.POST.get('ename')
                    emp_phone_num = request.POST.get('emp-phone-num')
                    emp_department = request.POST.get('emp-department')
                    emp_dob = request.POST.get('emp-dob')
                    emp_salary = request.POST.get('emp-salary')
                    emp_email = request.POST.get('emp-email')
                    emp_pwd = request.POST.get('emp-pwd')
                    employee = Employee.objects.create(
                        emp_id=emp_id, 
                        b_id=branch, 
                        emp_name=ename,
                        emp_phone_no=emp_phone_num,
                        department=emp_department,
                        dob=emp_dob,
                        salary=emp_salary,
                        emp_email=emp_email,
                        emp_password=emp_pwd
                    )   
                    return render(request, "all/add-employee.html", context=context)
                else:
                    return render(request, "all/add-employee.html", context=context)
    return redirect('/logincompany')

def edit_emp(request,emp_id):
    context = {}
    if 'company' in request.session:
        user = Company.objects.filter(c_id=request.session['company'])
        if user.exists():
                company_branches = Branch.objects.filter(company=request.session['company'])
                all_branches=[]
                for branch in company_branches:
                    all_branches.append(branch.b_id)
                context['company_branches']=all_branches
                context['emp_details']=Employee.objects.get(pk=emp_id)
                if request.method == 'POST':
                    branch_id = request.POST.get('branch')
                    branch_id = branch_id[branch_id.find("(")+1:branch_id.find(")")]
                    ename = request.POST.get('ename')
                    emp_phone_num = request.POST.get('emp-phone-num')
                    emp_department = request.POST.get('emp-department')
                    emp_salary = request.POST.get('emp-salary')
                    branch = Branch.objects.get(b_id=branch_id)
                    employee = Employee.objects.get(pk=emp_id)

                    employee.emp_id = emp_id
                    employee.b_id = branch
                    employee.emp_name = ename
                    employee.emp_phone_no = emp_phone_num
                    employee.department = emp_department
                    employee.salary = emp_salary
                    
                    employee.save()

                    return render(request, "all/edit-employee.html", context=context)
                else:
                    return render(request, "all/edit-employee.html", context=context)
    return redirect('/logincompany')

def all_emps(request):
    context = {}
    if 'company' in request.session:
        user = Company.objects.filter(c_id=request.session['company'])
        company=Company.objects.get(pk=request.session['company'])
        if user.exists():
            context['email'] = request.session['email']
            company_branches = Branch.objects.filter(company=request.session['company'])
            all_emps=[]
            for branch in company_branches:
                all_emps.extend(Employee.objects.filter(b_id=branch))
            context['all_emps']=all_emps
            return render(request,"all/all-employees.html",context=context)
    return redirect("/logincompany")
    
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
    return render(request,"all/modify_item_details.html",{})

def modify_stock(request):
    return render(request,"all/modify_stock.html",{})

def transaction(request):
    return render(request,"all/transaction.html",{})

def add_item(request):
    return render(request,"all/add_itm.html",{})

def source_items(request):
    context={}
    search_str=""
    if request.method == 'POST':
        search_str=request.POST.get('search_box')
    items=S_Products.objects.filter(p_name__regex=search_str)
    context['items']=items
    return render(request,"all/source_items.html",context=context)

def customerpage(request,):
    context={}
    if 'cus' in request.session:
        user = Customers.objects.filter(cus_id=request.session['cus'])
        if len(user)>0:
            context['email']=request.session['email']
            context['items']=Transaction.objects.filter(cus_id=request.session['cus'])
            return render(request,"all/customer-page.html",context=context)
    return redirect("/logincus")
    
def transaction_details(request,t_id):
    context={}
    if 'cus' in request.session:
        context['items']=Transaction.objects.filter(t_id=t_id)
        if len(context['items'])<1 or str(request.session['cus'])!=str(context['items'][0].cus_id.cus_id):
            return redirect('/logincus')
        else:
            orders_data=Orders.objects.filter(t_id=t_id)
            context['items']={} 
            for item in orders_data:
                temp_name=S_Products.objects.filter(p_id=item.p_id.p_id)
                if len(temp_name)>0:
                    context['items'][temp_name[0].p_name]=item.p_id.quantity
            print(context['items'])
            return render(request,"all/transaction_details.html",context=context)
    return redirect('/logincus')



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