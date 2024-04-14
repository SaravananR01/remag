from django.contrib import admin
from .models import *
import inspect

# for name, obj in inspect.getmembers(globals()):
#     if inspect.isclass(obj) and issubclass(obj, models.Model):
#         admin.site.register(obj)
models_arr=[Company,Branch,Warehouse,Store,W_Products,S_Products,Employee,Customers,Transaction,Orders]
for i in models_arr:
    admin.site.register(i)
