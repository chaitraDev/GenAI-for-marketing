from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
def landing_view(request):
    
    return render(request,"test.html")


def report_view(request):
    return render(request,"GenAi.html")

def dashboard_view(request):
    return render(request,'visuals.html')

def login_view(request):
    print("Login_view")
    if request.method=='POST':
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
                login(request,user)
                return HttpResponse("Sucessfully login")
    else:
        form = AuthenticationForm()  
             
def form(request):
     return render(request,"form.html")
