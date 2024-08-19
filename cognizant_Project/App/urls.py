from django.contrib import admin
from django.urls import path
from . import views
app_name="App"
urlpatterns = [
    path("",views.landing_view,name="Home"),
    path("dashboard/",views.dashboard_view,name="Dashboard"),
    path("report/",views.report_view,name="Report"),
    path("login/",views.login_view,name="Login"),
    path("form/",views.form,name="form")
]