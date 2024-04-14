from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logincompany", views.company_login, name="logincompany"),
    path("loginemp", views.emp_login, name="loginemp"),
    path("logincus", views.cus_login, name="logincus"),
    path("signupcompany", views.company_signup, name="signupcompany"),
    path("signupcus", views.company_login, name="signupcus"),
    path("companypage", views.company_page, name="companypage"),
    path("logout",views.home,name="logout")
]