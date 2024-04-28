from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.hashers import check_password,make_password
from django.http import HttpResponseRedirect
from django.contrib.auth.password_validation import validate_password
import random,bcrypt,datetime,time

'''
c_id              C   Company
b_id              B   Branch
s_id              S   Store
w_id              W   Warehouse
emp_id            E   Emp
cus_id            U   User
t_id              T   Transaction
o_id              O   Order
p_id              P   Product
'''

chars=[chr(x) for x in range (65,91)]
nums=[chr(x) for x in range (48,58)]

def gen_c_id():
    code="C"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    while len(Company.objects.filter(c_id=code))>0:
        code="C"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    return code

def gen_b_id():
    code="B"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    while len(Branch.objects.filter(b_id=code))>0:
        code="B"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    return code

def gen_s_id():
    code="S"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    while len(Store.objects.filter(s_id=code))>0:
        code="S"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    return code

def gen_w_id():
    code="W"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    while len(Warehouse.objects.filter(w_id=code))>0:
        code="W"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    return code

def gen_e_id():
    code="E"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    while len(Employee.objects.filter(emp_id=code))>0:
        code="E"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    return code

def gen_u_id():
    code="U"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    while len(Customers.objects.filter(cus_id=code))>0:
        code="U"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    return code

def gen_t_id():
    code="T"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    while len(Transaction.objects.filter(t_id=code))>0:
        code="T"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    return code

def gen_o_id():
    code="O"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    while len(Orders.objects.filter(o_id=code))>0:
        code="O"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    return code

def gen_p_id():
    code="P"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    while len(S_Products.objects.filter(p_id=code))>0 or len(W_Products.objects.filter(p_id=code))>0:
        code="P"+random.choice(nums)+random.choice(nums)+random.choice(chars)+random.choice(chars)
    return code

def check_password(password,hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def home(request):
    request.session.clear()
    request.session.flush()
    context={}
    if 'email' in context:
        context['email']=request.session['email']
    return render(request, "all/home.html",context)

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
                        c_id=gen_c_id(),
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
                            cus_id=gen_u_id(),
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
        context['email']=request.session['email']
        context['company']=Company.objects.get(pk=request.session['company'])
        context['branches']=Branch.objects.filter(company=request.session['company'])
        return render(request, "all/company-branches.html", context=context)
    return redirect("/logincompany")

def add_branch(request):
    context = {}
    if 'company' in request.session:
        context['email']=request.session['email']
        company=Company.objects.get(pk=request.session['company'])
        b_id=gen_b_id()
        context['branch_id']=b_id
        context['company_id']=company.c_id
        if request.method == 'POST':
                b_address=request.POST.get('address')
                b_phone_no=request.POST.get('phone-no')
                if (not b_phone_no.isdigit()) or (len(b_phone_no)!=10):
                    context['error']="Invalid phone number."
                else:
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

def branch_page(request,b_id):
    context = {}
    if 'company' in request.session:
        context['email']=request.session['email']
        context['company']=Company.objects.get(pk=request.session['company'])
        context['branch']=Branch.objects.get(pk=b_id)
        context['stores']=Store.objects.filter(branch=context['branch'])
        context['warehouses']=Warehouse.objects.filter(branch=context['branch'])
    return render(request,"all/company-page.html",context)

def delete_branch(request,b_id):
    context={}
    if 'company' in request.session:
        context['email']=request.session['email']
        context['id']=b_id
        context['type']="branch"
        context['redirect']="companypage"
        if request.method == 'POST':
            branch=Branch.objects.get(b_id=b_id)
            branch.delete()
            return redirect("/companypage")
        return render(request,"all/delete-misc.html",context)
    return redirect("/companypage")

def delete_shop(request,b_id,s_id):
    context={}
    if 'company' in request.session:
        context['email']=request.session['email']
        context['id']=s_id
        context['type']="store"
        context['redirect']=f"branch/{b_id}"
        if request.method == 'POST':
            store=Store.objects.get(s_id=s_id)
            store.delete()
            return redirect(f"/branch/{b_id}")
        return render(request,"all/delete-misc.html",context)
    return redirect("/companypage")

def delete_warehouse(request,b_id,w_id):
    context={}
    if 'company' in request.session:
        context['email']=request.session['email']
        context['id']=w_id
        context['type']="warehouse"
        context['redirect']=f"branch/{b_id}"
        if request.method == 'POST':
            warehouse=Warehouse.objects.get(w_id=w_id)
            warehouse.delete()
            return redirect(f"/branch/{b_id}")
        return render(request,"all/delete-misc.html",context)
    return redirect("/companypage")


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
                emp_id=gen_e_id()
                context['emp_id']=emp_id    
                if request.method == 'POST':
                    emp_id=request.POST.get('emp-id')
                    branch_id=request.POST.get('branch')
                    branch=Branch.objects.get(b_id=branch_id)
                    employees=Employee.objects.filter(b_id=branch)
                    ename = request.POST.get('ename')
                    emp_phone_num = request.POST.get('emp-phone-num')
                    emp_department = request.POST.get('emp-department')
                    emp_dob = request.POST.get('emp-dob')
                    emp_salary = request.POST.get('emp-salary')
                    emp_email = request.POST.get('emp-email')
                    emp_pwd = request.POST.get('emp-pwd')
                    emp_cnfpass=request.POST.get('emp-cnf-pwd')
                    emp_emails=[]
                    for emp in employees:
                        emp_emails.append(emp.emp_email)
                    if emp_dob!="":
                        emp_dob = datetime.datetime.strptime(emp_dob, '%Y-%m-%d').date()
                    if emp_pwd!=emp_cnfpass:
                        context['error']="PASSWORDS DO NOT MATCH!"
                        return render(request, "all/add-employee.html", context=context)
                    else:
                        if ename=="" or emp_phone_num==""  or emp_dob=="" or emp_email=="" or emp_pwd=="" or emp_department=="" or emp_salary=="":
                            context['error']="Blank Fields are not allowed."
                        elif emp_dob.year>datetime.date.today().year or emp_dob.year<datetime.date.today().year-100:
                            context['error']="Invalid date of birth."
                        elif (not emp_phone_num.isdigit()) or (len(emp_phone_num)!=10):
                            context['error']="Invalid phone number."
                        elif (emp_email in emp_emails):
                            context['error']="Email already exists."
                        else:
                            try:
                                validate_password(emp_pwd)
                            except Exception as e:
                                context['error']="Please use a stronger password. "+" ".join(e)
                            else:
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
                                return redirect('/all-employees')
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

def add_shop(request,b_id):
    context={}
    if 'company' in request.session:
        new_s_id=gen_s_id()
        Store.objects.create(
            branch=Branch.objects.get(b_id=b_id),
            s_id=new_s_id,
        )
        return redirect(f'/branch/{b_id}')
    return redirect('/')

def add_warehouse(request,b_id):
    context={}
    if 'company' in request.session:
        new_w_id=gen_w_id()
        Warehouse.objects.create(
            branch=Branch.objects.get(b_id=b_id),
            w_id=new_w_id,
        )
        return redirect(f'/branch/{b_id}')
    return redirect('/')

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
            context['emp']=user[0]
            context['branch']=user[0].b_id
            request.session.pop('t_id',None)
            request.session.pop('trx_items',None)
            request.session.modified=True
            return render(request,"all/employee-page.html",context=context)
    return redirect("/loginemp")
    
def modify_stock_emp(request):
    context={}
    if 'emp' in request.session:
        user = Employee.objects.filter(emp_id=request.session['emp'])
        context['email']=request.session['email']
        if len(user)>0:
            context['email']=request.session['email']
            context['emp']=user[0]
            context['branch']=user[0].b_id
            context['stores']=Store.objects.filter(branch=context['branch'])
            context['warehouses']=Warehouse.objects.filter(branch=context['branch'])
            return render(request,"all/modify-stock-emp.html",context=context)
    return redirect("/loginemp")

#commenting just in case we change our minds or rm it
# def modify_item_details(request,b_id,id,pid):
#     context={}
#     if 'company' in request.session:
#         user=Company.objects.filter(c_id=request.session['company'])
#         if user.exists():
#             context['email']=request.session['email']
#             context['id']=id
#             context['b_id']=b_id
#             context['pid']=pid
#             if (id[0]=="S"):
#                 product=S_Products.objects.get(pk=pid)
#                 context['product']=product
#             elif (id[0]=="W"):
#                 product=W_Products.objects.get(pk=pid)
#                 context['product']=product
#             return render(request,"all/modify_item_details.html",context)

#     return redirect("/")

def modify_stock(request,b_id,id):
    context={}
    if 'company' in request.session:
        user=Company.objects.filter(c_id=request.session['company'])
        if user.exists():
            context['email']=request.session['email']
            context['id']=id
            context['b_id']=b_id
            all_products=[]
            branch=Branch.objects.get(pk=b_id)
            if (id[0]=="S"):
                stores=Store.objects.filter(branch=branch)
                for store in stores:
                    if store.s_id==id:
                        s_products=S_Products.objects.filter(s_id=id)
                        for product in s_products:
                            all_products.append(product)
                        context['all_products']=all_products

            elif (id[0]=="W"):
                warehouses=Warehouse.objects.filter(branch=branch)
                for warehouse in warehouses:
                    if warehouse.w_id==id:
                        w_products=W_Products.objects.filter(w_id=id)
                        for product in w_products:
                            all_products.append(product)
                        context['all_products']=all_products
            return render(request,"all/modify_stock.html",context)
    return redirect("/logincompany")


def emp_modify_stock(request,b_id,id):
    context={}
    if 'emp' in request.session:
        user=Employee.objects.filter(emp_id=request.session['emp'])
        if user.exists():
            context['email']=request.session['email']
            context['id']=id
            context['b_id']=b_id
            all_products=[]
            branch=Branch.objects.get(pk=b_id)
            if (id[0]=="S"):
                stores=Store.objects.filter(branch=branch)
                for store in stores:
                    if store.s_id==id:
                        s_products=S_Products.objects.filter(s_id=id)
                        for product in s_products:
                            all_products.append(product)
                        context['all_products']=all_products

            elif (id[0]=="W"):
                warehouses=Warehouse.objects.filter(branch=branch)
                for warehouse in warehouses:
                    if warehouse.w_id==id:
                        w_products=W_Products.objects.filter(w_id=id)
                        for product in w_products:
                            all_products.append(product)
                        context['all_products']=all_products
            return render(request,"all/emp_modify_stock.html",context)
    return redirect("/loginemp")


def transaction(request):
    context={}
    if 'emp' in request.session:
        user = Employee.objects.filter(emp_id=request.session['emp'])
        if len(user)>0:
            context['email']=request.session['email']
            context['total_cost']=0
            if 't_id'  not in request.session:
                request.session['t_id']=gen_t_id()
                request.session.modified=True
            context['t_id']=request.session['t_id']
            if 'trx_items' in request.session:
                class TrxItm():
                    def __init__(self,id,name,price,qty):
                        self.id=id
                        self.name=name
                        self.price=price
                        self.qty=qty
                        self.cost=price*qty


                context['items']=[]

                for item in request.session['trx_items']:
                    prod=S_Products.objects.get(pk=item)
                    itm=TrxItm(prod.p_id,prod.p_name,prod.price,request.session['trx_items'][item])
                    context['items'].append(itm)
                    context['total_cost']+=itm.cost
            else:
                context['items']={}
            if request.method == 'POST':
                cus_id=request.POST['cus_id']
                cus=Customers.objects.filter(cus_id=cus_id)
                print(cus_id,cus)
                if len(cus)!=1:
                    context['error']="Invalid customer id!"
                else:
                    if 'trx_items' in request.session and len(context['items'])>0:
                        new_trx=Transaction.objects.create(
                            t_id=request.session['t_id'],
                            emp_id=user[0],
                            date_of_transaction=datetime.datetime.now(),
                            cus_id=cus[0],
                            total_cost=context['total_cost'],
                        )
                        for item in context['items']:
                            sprod=S_Products.objects.get(pk=item.id)
                            sprod.quantity-=item.qty
                            sprod.save()
                            new_odr=Orders.objects.create(
                                o_id=gen_o_id(),
                                t_id=new_trx,
                                p_id=sprod,
                                quantity=item.qty,
                            )
                        return redirect('/emp-page')
                    else:
                        context['error']="Add some items first."
        return render(request,"all/transaction.html",context)
    return redirect("/loginemp")

def add_item(request,b_id,id):
    context={}
    if 'company' in request.session:
        user=Company.objects.filter(c_id=request.session['company'])
        if user.exists():
            context['id']=id
            context['b_id']=b_id
            context['email']=request.session['email']
            p_id=gen_p_id()
            context['p_id']=p_id
            if request.method=="POST":
                p_id=request.POST.get("p_id")
                p_name=request.POST.get("p_name")
                p_manu=request.POST.get("p_manu")
                price=request.POST.get("price")
                m_date=request.POST.get("m_date")
                e_date=request.POST.get("e_date")
                quantity=request.POST.get("quantity")
                branch=Branch.objects.get(pk=b_id)
                if (id[0]=="S"):
                    s_id=Store.objects.get(pk=id)
                    S_Products.objects.create(
                        p_id=p_id,
                        s_id=s_id,
                        p_name=p_name,
                        p_manufacturer=p_manu,
                        price=price,
                        mfg_date=m_date,
                        expiry_date=e_date,
                        quantity=quantity
                    )
                elif (id[0]=="W"):
                    w_id=Warehouse.objects.get(pk=id)
                    W_Products.objects.create(
                        p_id=p_id,
                        w_id=w_id,
                        p_name=p_name,
                        p_manufacturer=p_manu,
                        price=price,
                        mfg_date=m_date,
                        expiry_date=e_date,
                        quantity=quantity
                    )
                return redirect("/modify-stock/"+b_id+"/"+id)
            return render(request,"all/add_itm.html",context) 
    return redirect("/logincompany")

def add_item_emp(request,b_id,id):
    context={}
    if 'emp' in request.session:
        user= Employee.objects.filter(emp_id=request.session['emp'])
        if user.exists():
            context['id']=id
            context['b_id']=b_id
            context['email']=request.session['email']
            p_id=gen_p_id()
            context['p_id']=p_id
            context['address']="/modify-stock-emp"
            if request.method=="POST":
                p_id=request.POST.get("p_id")
                p_name=request.POST.get("p_name")
                p_manu=request.POST.get("p_manu")
                price=request.POST.get("price")
                m_date=request.POST.get("m_date")
                e_date=request.POST.get("e_date")
                quantity=request.POST.get("quantity")
                branch=Branch.objects.get(pk=b_id)
                if (id[0]=="S"):
                    s_id=Store.objects.get(pk=id)
                    S_Products.objects.create(
                        p_id=p_id,
                        s_id=s_id,
                        p_name=p_name,
                        p_manufacturer=p_manu,
                        price=price,
                        mfg_date=m_date,
                        expiry_date=e_date,
                        quantity=quantity
                    )
                elif (id[0]=="W"):
                    w_id=Warehouse.objects.get(pk=id)
                    W_Products.objects.create(
                        p_id=p_id,
                        w_id=w_id,
                        p_name=p_name,
                        p_manufacturer=p_manu,
                        price=price,
                        mfg_date=m_date,
                        expiry_date=e_date,
                        quantity=quantity
                    )
                return redirect("/emp-modify-stock/"+b_id+"/"+id)
            return render(request,"all/add_itm_emp.html",context)    
    return redirect("/loginemp")  

def delete_product(request,b_id,id,p_id):
    context={}
    if 'company' in request.session:
        context['email']=request.session['email']
        context['id']=p_id
        context['type']="product"
        context['redirect']="modify-stock/"+b_id+"/"+id
        if request.method == 'POST':
            if (id[0]=="S"):
                store=Store.objects.get(pk=id)
                products=S_Products.objects.filter(s_id=store)
                for product in products:
                    if product.p_id==p_id:
                        product.delete()
            elif (id[0]=="W"):
                warehouse=Warehouse.objects.get(pk=id)
                products=W_Products.objects.filter(w_id=warehouse)
                for product in products:
                    if product.p_id==p_id:
                        product.delete()
            return redirect("/modify-stock/"+b_id+"/"+id)
        return render(request,"all/delete-misc.html",context)
    return redirect("/companypage")

def delete_product_emp(request,b_id,id,p_id):
    context={}
    if 'emp' in request.session:
        context['email']=request.session['email']
        context['id']=p_id
        context['type']="product"
        context['redirect']="modify-stock/"+b_id+"/"+id
        if request.method == 'POST':
            if (id[0]=="S"):
                store=Store.objects.get(pk=id)
                products=S_Products.objects.filter(s_id=store)
                for product in products:
                    if product.p_id==p_id:
                        product.delete()
            elif (id[0]=="W"):
                warehouse=Warehouse.objects.get(pk=id)
                products=W_Products.objects.filter(w_id=warehouse)
                for product in products:
                    if product.p_id==p_id:
                        product.delete()
            return redirect("/emp-modify-stock/"+b_id+"/"+id)
        return render(request,"all/delete-misc.html",context)
    return redirect("/loginemp")


def add_transaction_item(request):
    context={}
    if 'emp' in request.session:
        user = Employee.objects.filter(emp_id=request.session['emp'])
        if len(user)>0:
            context['email']=request.session['email']
            context['total_cost']=0
            if 't_id'  not in request.session:
                request.session['t_id']=gen_t_id()
                request.session.modified=True
            context['t_id']=request.session['t_id']
            if 'trx_items' in request.session:
                class TrxItm():

                    def __init__(self,id,name,price,qty):
                        self.id=id
                        self.name=name
                        self.price=price
                        self.qty=qty
                        self.cost=price*qty


                context['dummyitems']=[]

                for item in request.session['trx_items']:
                    prod=S_Products.objects.get(pk=item)
                    itm=TrxItm(prod.p_id,prod.p_name,prod.price,request.session['trx_items'][item])
                    context['dummyitems'].append(itm)
                    context['total_cost']+=itm.cost
            else:
                context['dummyitems']={}
            if request.method == 'POST':
                valid_stores=Store.objects.filter(branch=user[0].b_id)
                items=S_Products.objects.filter(p_name__iregex=request.POST.get('item-name'),s_id__in=valid_stores)
                context['items']=items
        return render(request,"all/add-transaction-item.html",context)  
    return redirect("/loginemp")

def add_item_trx(request,p_id,qty):
    if 'emp' in request.session:
        user = Employee.objects.filter(emp_id=request.session['emp'])
        if len(user)>0:
            prod=S_Products.objects.get(pk=p_id)
            if 'trx_items' in request.session:
                    if p_id in request.session['trx_items']:
                        if qty<0 or qty+request.session['trx_items'][p_id]>prod.quantity:
                            pass
                        else:
                            request.session['trx_items'][p_id]+=qty
                    else:
                        if qty<0 or qty>prod.quantity:
                            pass
                        else:
                            request.session['trx_items'][p_id]=qty
            else:
                if qty<0 or qty>prod.quantity:
                    request.session['trx_items']={}
                else:
                    request.session['trx_items']={p_id:qty}
    request.session.modified=True
    return redirect('/transaction')

def del_item_trx(request,p_id):
    if 'emp' in request.session:
        user = Employee.objects.filter(emp_id=request.session['emp'])
        if len(user)>0:
            prod=S_Products.objects.get(pk=p_id)
            if 'trx_items' in request.session:
                    if p_id in request.session['trx_items']:
                        request.session['trx_items'].pop(p_id)
            else:
                    request.session['trx_items']={}
    request.session.modified=True
    return redirect('/transaction')

def source_items(request):
    context={}
    search_str=""
    if request.method == 'POST':
        search_str=request.POST.get('search_box')
        items=S_Products.objects.filter(p_name__iregex=search_str)
        context['items']=items
    return render(request,"all/source_items.html",context=context)

def customerpage(request):
    context={}
    if 'cus' in request.session:
        user = Customers.objects.filter(cus_id=request.session['cus'])
        if len(user)>0:
            context['email']=request.session['email']
            context['cus']=user[0]
            context['items']=Transaction.objects.filter(cus_id=request.session['cus'])
            return render(request,"all/customer-page.html",context=context)
    return redirect("/logincus")
    
def transaction_details(request,t_id):
    context={}
    if 'cus' in request.session:
        context['items']={}
        trx=Transaction.objects.filter(pk=t_id)
        if len(trx)<1 or str(request.session['cus'])!=str(trx[0].cus_id.cus_id):
            return redirect('/logincus')
        else:
            trx=trx[0]
            orders_data=Orders.objects.filter(t_id=trx)
            print(orders_data)
            context['items']={} 
            for item in orders_data:
                temp_name=item.p_id
                print(temp_name)
                context['items'][temp_name.p_name]=item.quantity
            print(context['items'])
            return render(request,"all/transaction_details.html",context=context)
    return redirect('/logincus')

def logout(request):
    request.session.clear()
    request.session.flush()
    return redirect('/')

