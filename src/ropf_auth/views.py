from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import LoginForm

# Create your views here.
# def login_page(request):
#     return render(request, "ropf_auth/login.html" , {})

def login_page(request):

    form=LoginForm(request.POST or None)
    print(request.POST)
    default_password_list=["Voda_1234"]
    context = {
        "form": form
    }
    # print(form.is_valid())
    # print("User logged in")

    #print(request.user.has_perm)
    # print(request.user.is_staff)
    #print(123)
    if form.is_valid():
        # print(123)
        #print(form.cleaned_data)
        username=str(form.cleaned_data.get("username").lower())
        password = str(form.cleaned_data.get("password"))
        #user=ntlogin(username,password)
        user = authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
            existing_pass=User.objects.get(username=username).password
            login(request, user)

            if password not in default_password_list:

                login(request,user)
            else:
                return redirect ("new_password/")

            context['form']=LoginForm()
            return redirect("welcome/")
        #     if  request.user.is_staff:
        #         return redirect("welcome/")
        #         # print("staff")
        #     else:
        #         return redirect("welcome/")
        #         # print("users")
        else:
            print(username)
            if  not User.objects.filter(username=username).exists():
                context.update({"user_na":"success"})
            else:
                context.update({"wrong_pass":"success"})
            # print("Error")
        print(context)
    return render(request,"ropf_auth/login.html",context)
@login_required(login_url='/')
def welcome(request):
    user_name = request.user.username

    context = {"username": user_name, "user_region": "None"}
    return render(request,"ropf_auth/welcome.html",context)

def register_page(request):
    return render(request, "ropf_auth/register.html" , {})
@login_required(login_url='/')
def auth_error_page(request):
    user_name = request.user.username

    context = {"username": user_name, "user_region": "None"}
    return render(request, "ropf_auth/auth_error.html" , context)
@login_required(login_url='/')
def logout_page(request):
    print("logout")
    logout(request)
    return redirect("/")

@login_required(login_url='/')
def new_pass(request):
    if request.method == 'POST' and ("new_pass" in request.POST):
        username = request.user.username
        print(username)
        new_pass = request.POST.get("new_password")
        print(new_pass)
        confirm_pass = request.POST.get("confirm_pass")
        print(confirm_pass)
        if len(new_pass)<8:
            return render(request, "ropf_auth/new_pass.html" , {"pass":"criteria_missmatch"})
        if new_pass == confirm_pass:
            # u=User.objects.get(username="anabawy")
            # u.set_password("Voda_1234")
            # u.save()
            # print("Done")
            u = User.objects.get(username=username)
            u.set_password(new_pass)
            u.save()
            user = authenticate(request, username=username, password=new_pass)
            login(request, user)
            print("Done")
            return redirect("/welcome/")
    return render(request, "ropf_auth/new_pass.html" , {})


@staff_member_required
def admin_page(request):
    context={}
    if request.method == 'POST' and ("reset_pass" in request.POST):
        username=request.POST.get("username")
        if User.objects.filter(username=username).exists():
            print("Done")
            u=User.objects.get(username=username)
            u.set_password("Voda_1234")
            u.save()
            context={"username":username,"user_name":"exist"}

        else:
            context={"username":username,"user_name":"not_exist"}
    return render(request, "ropf_auth/ropf_admin.html",context)