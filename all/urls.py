from django.urls import path,include, re_path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logincompany", views.company_login, name="logincompany"),
    path("loginemp", views.emp_login, name="loginemp"),
    path("logincus", views.cus_login, name="logincus"),
    path("signupcompany", views.company_signup, name="signupcompany"),
    path("signupcus", views.cus_signup, name="signupcus"),
    path("companypage", views.company_page, name="companypage"),
    path("all-employees",views.all_emps,name="all-emps"),
    path("branchpage", views.branch_page, name="branchpage"),
    path("add-emp", views.add_emp, name="add-emp"),
    path("edit-emp/<str:emp_id>", views.edit_emp, name="edit-emp"),
    path("add-branch", views.add_branch, name="add-branch"),
    path("edit-shop", views.edit_shop, name="edit-shop"),
    path("emp-page", views.emp_page, name="emp-page"),
    path("modify-item-details", views.modify_item_details, name="modify-item-details"),
    path("modify-stock", views.modify_stock, name="modify-stock"),
    path("transaction-details/<str:t_id>", views.transaction_details, name="transaction-details"),
    path("transaction", views.transaction, name="transaction"),
    path("add-item", views.add_item, name="add-item"),
    path("source-item", views.source_items, name="source-item"),
    path("customer", views.customerpage, name="customer"),
    path("edit-warehouse", views.edit_warehouse, name="edit-warehouse"),
    path("store-form",views.changeshop,name="store-form"),
    path("warehouse-form",views.changewarehouse,name="warehouse-form"),
    path("signupcus", views.cus_signup, name="signupcus"),
    path("companypage", views.company_page, name="companypage"),
    path("logout",views.logout,name="logout")
]