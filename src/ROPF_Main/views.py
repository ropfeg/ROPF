from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from shutil import copyfile
from django.contrib.admin.views.decorators import staff_member_required
import pandas as pd
# from django_tables2.config import RequestConfig
# from django_tables2.export.export import TableExport


def home_page(request):
    return render(request, "login.html" , {})

def under_construction(request):
    user_name = request.user.username

    context = {"username": user_name, "user_region": "None"}
    return render(request,"under_construction.html",context)

# def session_details(request):
#     s = Session.objects.all()
#
#     df=pd.DataFrame()
#     user_name=[]
#     last_login_list=[]
#     expire_date=[]
#     expire_time=[]
#     for i in s:
#         session_expire_date=i.expire_date
#         session_data=i.get_decoded()
#         user_id=int(session_data["_auth_user_id"])
#         print(type(user_id))
#
#         u_exisitance= User.objects.filter(id=user_id).exists()
#         print(u_exisitance)
#
#         print(session_expire_date.time())
#         print("username")
#         if u_exisitance:
#             u = User.objects.filter(id=user_id).values('username')
#             last_login=User.objects.get(id=user_id).last_login
#             u=u[0]["username"]
#             user_name.append(u)
#             last_login_list.append(last_login.date())
#             expire_date.append(session_expire_date.date())
#             expire_time.append(session_expire_date.time())
#             print(last_login)
#             print(u)
#             print(session_expire_date.date())
#             print(session_expire_date.time())
#     df["Usernmae"]=user_name
#     df["Last_login"]=last_login_list
#     df["SessionDate"]=expire_date
#     df["SessionTime"] = expire_time
#     print(df)
#     df.to_excel("session_test.xlsx")
#
#     return render(request, "test.html" , {})


@staff_member_required
def admin_page(request):
    context={}
    print("hi")
    s = Session.objects.all()
    users=User.objects.all()
    df=pd.DataFrame()
    user_name=[]
    last_login_list=[]
    # expire_date=[]
    # expire_time=[]
    for user in users:
        # session_expire_date=i.expire_date
        # session_data=i.get_decoded()
        # user_id=int(session_data["_auth_user_id"])
        # print(type(user_id))

        # u_exisitance= User.objects.filter(id=user_id).exists()
        # print(u_exisitance)

        # print(session_expire_date.time())
        # print("username")
        # if u_exisitance:
        # u = User.objects.filter(id=user).values('username')
        last_login=User.objects.get(username=user).last_login
        # u=u[0]["username"]
        user_name.append(user)
        if not (last_login is None):
            last_login_list.append(last_login.date())
        else:
            last_login_list.append(last_login)
        # expire_date.append(session_expire_date.date())
        # expire_time.append(session_expire_date.time())
        # print(last_login)
        # print(u)
        print(user)
        print(last_login)
            # print(session_expire_date.date())
            # print(session_expire_date.time())
    df["Usernmae"]=user_name
    df["Last_login"]=last_login_list
    # # df["SessionDate"]=expire_date
    # # df["SessionTime"] = expire_time
    # print(df)
    df.to_excel("./static/session_test.xlsx")
    copyfile("./db.sqlite3", "./static/db.sqlite3")
    if request.method == 'POST' and ("reset_pass" in request.POST):
        username = str(request.POST.get('username').lower())

        if User.objects.filter(username=username).exists():
            print("change password")
            u = User.objects.get(username=username)
            u.set_password("Voda_1234")
            u.save()
            context.update({"user_name": "exist"})

        else:
            context.update({"user_name": "not_exist"})
            print("doesn't exists in database")


    return render(request, "ropf_admin.html" , context)


# def table_view(request):
#     table = MyTable(Person.objects.all())
#
#     RequestConfig(request).configure(table)
#
#     export_format = request.GET.get("_export", None)
#     if TableExport.is_valid_format(export_format):
#         exporter = TableExport(export_format, table)
#         return exporter.response("table.{}".format(export_format))
#
#     return render(request, "table.html", {
#         "table": table
#     })