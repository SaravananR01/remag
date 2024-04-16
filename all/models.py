from django.db import models
#from django.contrib.auth.hashers import make_password
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()  # Generate a random salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

class Company(models.Model):
    c_id=models.CharField(primary_key=True,max_length=5)
    c_name=models.CharField(max_length=30,null=False)
    c_phone=models.IntegerField(null=False)
    c_address=models.CharField(max_length=200,null=False)
    c_email=models.CharField(null=False,max_length=30)
    c_password=models.CharField(null=False,max_length=200)

    def save(self, *args, **kwargs):
        self.c_password = hash_password(self.c_password)
        super(Company, self).save(*args, **kwargs)

class Branch(models.Model):
    b_id=models.CharField(primary_key=True,max_length=5)
    c_id=models.ForeignKey(Company, on_delete=models.CASCADE)
    b_address=models.CharField(null=False,max_length=200)
    b_phone_no=models.IntegerField(null=False)

class Warehouse(models.Model):
    w_id=models.CharField(primary_key=True,max_length=5)
    b_id=models.ForeignKey(Branch,on_delete=models.CASCADE)
    w_admin_id=models.CharField(null=True,max_length=5)

class Store(models.Model):
    s_id=models.CharField(primary_key=True,max_length=5)
    b_id=models.ForeignKey(Branch,on_delete=models.CASCADE)
    s_admin_id=models.CharField(null=True,max_length=5)

class W_Products(models.Model):
    p_id=models.CharField(primary_key=True,max_length=5)
    w_id=models.ForeignKey(Warehouse,on_delete=models.CASCADE)
    p_name=models.CharField(null=False,max_length=30)
    p_manufacturer=models.CharField(max_length=30,null=False)
    price=models.IntegerField(null=False)
    mfg_date=models.DateField(null=False)
    expiry_date=models.DateField(null=False)
    quantity=models.IntegerField(null=False)

class S_Products(models.Model):
    p_id=models.CharField(primary_key=True,max_length=5)
    s_id=models.ForeignKey(Store,on_delete=models.CASCADE)
    p_name=models.CharField(null=False,max_length=30)
    p_manufacturer=models.CharField(max_length=30,null=False)
    price=models.IntegerField(null=False)
    mfg_date=models.DateField(null=False)
    expiry_date=models.DateField(null=False)
    quantity=models.IntegerField(null=False)

class Employee(models.Model):
    emp_id=models.CharField(primary_key=True,max_length=5)
    b_id=models.ForeignKey(Branch,on_delete=models.CASCADE)
    emp_name=models.CharField(max_length=40,null=False)
    emp_phone_no=models.IntegerField(null=False)
    department=models.CharField(max_length=30)
    dob=models.DateField(null=False)
    salary=models.IntegerField(null=False)
    emp_email=models.CharField(null=False,max_length=30)
    emp_password=models.CharField(null=False,max_length=200)

    def save(self, *args, **kwargs):
        self.emp_password = hash_password(self.emp_password)
        super(Employee, self).save(*args, **kwargs)

# class Departments(models.Model):
#     dept_id=models.CharField(primary_key=True)
#     b_id=models.ForeignKey(Branch,on_delete=models.CASCADE)
#     d_head_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
#     d_name=models.CharField(null=False)
#     d_size=models.IntegerField()

class Customers(models.Model):
    cus_id=models.CharField(primary_key=True,max_length=5)
    cus_name=models.CharField(max_length=30)
    cus_join_date=models.DateField(null=False)
    cus_points=models.IntegerField(null=False)
    dob= models.DateField(null=False)
    cus_phone_no=models.IntegerField()
    cus_email=models.CharField(null=False,max_length=30)
    cus_password=models.CharField(null=False,max_length=200)

    
    def save(self, *args, **kwargs):
        self.cus_password = hash_password(self.cus_password)
        super(Customers, self).save(*args, **kwargs)

class Transaction(models.Model):
    t_id=models.CharField(primary_key=True,max_length=5)
    emp_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
    date_of_transaction=models.DateField(null=False)
    cus_id=models.ForeignKey(Customers,on_delete=models.CASCADE)

class Orders(models.Model):
    o_id=models.CharField(primary_key=True,max_length=5)
    t_id=models.ForeignKey(Transaction,on_delete=models.CASCADE)
    p_id=models.ForeignKey(S_Products,on_delete=models.CASCADE)
    quantity=models.IntegerField(null=False)
