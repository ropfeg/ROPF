from django.shortcuts import render,redirect
from servant_app.models import general_info,tx_info,radio_info
from .models import power_info,civil_info
# from ropf_auth.models import Manager,SPOC,User,Super_User,UserProfile,HOD
from ropf_auth.models import user_privilege,UserProfile
from pandas import read_excel,Timestamp
import time
from django.contrib.auth.decorators import login_required
# Create your views here.
def site_hisory(request):
    context={}
    return render(request, "site_history/site_history.html", context)



def civil_info_page(request):
    context = {}
    if request.method == 'POST' and ("single_search" in request.POST):
        site = request.POST.get("site_id")
        print(site)
        existance = "incorrect"
        if general_info.objects.filter(site_id=site).exists():
            existance = "yes"
            site_gi = general_info.objects.filter(site_id=site).values()
            context.update({
                "site_id": site,
                "option": site_gi[0]["option"],
                "region": site_gi[0]["region"],

            })
            context["map"] = "https://maps.google.com/maps?q=" + str(site_gi[0]["latitude"]) + "%2C" + str(site_gi[0]["longitude"]) + "&t=k&z=15&ie=UTF8&iwloc=&output=embed"
        if civil_info.objects.filter(site_id=site).exists():
            existance = "yes"
            site_ci = civil_info.objects.filter(site_id=site).values()
            context.update({

                "RT_GF": site_ci[0]["RT_GF"],
                "st_type": site_ci[0]["ST_Type"],
                "height": site_ci[0]["Height"],
                "grillage": site_ci[0]["Grillage"],
                "anchoring": site_ci[0]["Anchoring"],
                "building": site_ci[0]["Building"],
                "new_requirement_details": site_ci[0]["new_requirement_details"],
                "project_name": site_ci[0]["Project_Name"],
                "site_status": site_ci[0]["Site_Status"],
                "Consultant_recommendations": site_ci[0]["Consultant_recommendations"],
                "remarks": site_ci[0]["Remarks"],

            })

        context.update({"site_search": existance})
    elif request.method == 'POST' and ("crq_update" in request.POST):
        start = time.time()
        myfile = request.FILES['myfile']
        print("start")
        df = read_excel(myfile)
        df[['Request_Date', 'Feed_back']] = df[
            ['Request_Date', 'Feed_back']].fillna(Timestamp('19900101'))
        df = df.fillna('0')
        data = []
        for ind in df.index:
            record = civil_info(
                site_id=df["site_id"][ind],
                Name=df["Name"][ind],
                Area=df["Area"][ind],
                Requester=df["Requester"][ind],
                Consultant_name=df["Consultant_name"][ind],
                New_requirement=df["New_requirement"][ind],
                new_requirement_details=df["new_requirement_details"][ind],
                attached_mail=df["attached_mail"][ind],
                Status=df["Status"][ind],
                EIC=df["EIC"][ind],
                Feed_back=df["Feed_back"][ind],
                Project_Name=df["Project_Name"][ind],
                Site_Status=df["Site_Status"][ind],
                RT_GF=df["RT_GF"][ind],
                ST_Type=df["ST_Type"][ind],
                Tower_Type=df["Tower_Type"][ind],
                Height=df["Height"][ind],
                Tower_body=df["Tower_body"][ind],
                Grillage=df["Grillage"][ind],
                Anchoring=df["Anchoring"][ind],
                Building=df["Building"][ind],
                Consultant_recommendations=df["Consultant_recommendations"][ind],
                Action_Taken=df["Action_Taken"][ind],
                Remarks=df["Remarks"][ind],
            )
            data.append(record)
        civil_info.objects.filter(all).delete()
        civil_info.objects.bulk_create(data)
        duration = time.time() - start
        print(duration)
        context = {"admin_risk_msg": "submit"}

    return render(request, "site_history/civil_info.html", context)





def power_info_page(request):
    context = {}
    if request.method == 'POST' and ("single_search" in request.POST):
        site = request.POST.get("site_id")
        print(site)
        existance = "incorrect"
        if general_info.objects.filter(site_id=site).exists():
            existance = "yes"
            site_gi = general_info.objects.filter(site_id=site).values()
            context.update({
                "site_id": site,
                "option": site_gi[0]["option"],
                "region": site_gi[0]["region"],

            })
            context["map"] = "https://maps.google.com/maps?q=" + str(site_gi[0]["latitude"]) + "%2C" + str(site_gi[0]["longitude"]) + "&t=k&z=15&ie=UTF8&iwloc=&output=embed"
        if power_info.objects.filter(site_id=site).exists():
            existance = "yes"
            site_pi = power_info.objects.filter(site_id=site).values()
            context.update({

                "site_vendor": site_pi[0]["Site_Vendor"],
                "PowerConumption": site_pi[0]["Power_Conumption"],
                "Generated_Power": site_pi[0]["Generated_Power"],
                "utilization": round((site_pi[0]["Power_Conumption"]/site_pi[0]["Generated_Power"]*100),0),
                "site_type": site_pi[0]["Site_Type"],
                "cabinets_type": site_pi[0]["Cabients_Type"],
                "Cabinet_num": site_pi[0]["Cabinet_Num"],
                "System_Voltage": site_pi[0]["System_Voltage"],
                "Power_Cabinet": site_pi[0]["Power_Cabinet"],
                "Rect_Count": site_pi[0]["Rect_Count"],
                "Battery_Type": site_pi[0]["Battery_Type"],
                "Bat_Count": site_pi[0]["Bat_Count"],

            })

            context.update({"site_search": existance})
    elif request.method == 'POST' and ("crq_update" in request.POST):
        start = time.time()
        myfile = request.FILES['myfile']
        print("start")
        df = read_excel(myfile)
        df = df.fillna('0')
        data = []
        for ind in df.index:
            record = power_info(
                Site_Name=df["Site_Name"][ind],
                site_id=df["site_id"][ind],
                Site_Vendor=df["Site_Vendor"][ind],
                Site_Region=df["Site_Region"][ind],
                Site_Type=df["Site_Type"][ind],
                Site_State=df["Site_State"][ind],
                Position=df["Position"][ind],
                Governate=df["Governate"][ind],
                Cabients_Type=df["Cabients_Type"][ind],
                Cabinet_Num=df["Cabinet_Num"][ind],
                Cabinet_Activity=df["Cabinet_Activity"][ind],
                System_Voltage=df["System_Voltage"][ind],
                Rectifier_Type=df["Rectifier_Type"][ind],
                Rect_Count=df["Rect_Count"][ind],
                Needed_Rectifiers=df["Needed_Rectifiers"][ind],
                Battery_Type=df["Battery_Type"][ind],
                Bat_Count=df["Bat_Count"][ind],
                Needed_Batteries=df["Needed_Batteries"][ind],
                Power_Cabinet=df["Power_Cabinet"][ind],
                Power_Conumption=df["Power_Conumption"][ind],
                Generated_Power=df["Generated_Power"][ind],
                FC_Comp_Name=df["FC_Comp_Name"][ind],
                FC_Comp_Count=df["FC_Comp_Count"][ind],
                Battery_cabinet=df["Battery_cabinet"][ind],
                Bat_Cab_Count=df["Bat_Cab_Count"][ind],
            )
            data.append(record)
        power_info.objects.bulk_create(data)
        duration = time.time() - start
        print(duration)
        context = {"admin_risk_msg": "submit"}
    return render(request, "site_history/power_info.html", context)




@login_required(login_url='/')
def site_info_page(request):

    user_name = request.user.username
    user_id = request.user.id
    # print(user_id)
    context = {"username":user_name,"user_region":"None"}
    # --------- start auth ------------
    if user_privilege.objects.filter(user_id=user_id).exists():

        if user_privilege.objects.get(user_id=user_id).site_history == "no":
            return redirect("/auth_error/")
        else:
            context.update({
                'userprivileges':user_privilege.objects.get(user_id=user_id).site_history,
                'read': ['r', 'cr', 'cru', 'crud'],
                'read_write': ['cr', 'cru', 'crud'],
                'cru': ['cru','crud'],
                'crud': ['crud']
            })





    if UserProfile.objects.filter(user_id=user_id).exists():

        userprofile = UserProfile.objects.get(user_id=user_id)
        print(userprofile)
        # print(userprofile.image.url)
        context.update({
                    "user_region":userprofile.user_region,
                    # "avatar":userprofile.image.url

        })
    # ----------- end auth ------------

    if request.method == 'POST' and ("single_search" in request.POST):
        site = request.POST.get("site_id")
        print(site)
        existance = "incorrect"
        if general_info.objects.filter(site_id=site).exists():
            existance = "yes"
            site_gi = general_info.objects.filter(site_id=site).values()
            # ------------   Start Region _authentication --------------
            if context["user_region"] in [site_gi[0]["region"],"All"]:
                pass
            else:
                context.update({"region_search_msg":"incorrect"})
                return render(request, "site_history/site_history_new.html", context)
            # ------------   End Region _authentication --------------
            context.update({
                "site_id": site,
                "option": site_gi[0]["option"],
                "region": site_gi[0]["region"],

            })
            context["map"] = "https://maps.google.com/maps?q=" + str(site_gi[0]["latitude"]) + "%2C" + str(site_gi[0]["longitude"]) + "&t=k&z=15&ie=UTF8&iwloc=&output=embed"
        if power_info.objects.filter(site_id=site).exists():
            print("enterpowerinfo")
            existance = "yes"
            site_pi = power_info.objects.filter(site_id=site).values()
            utilization =str(round((site_pi[0]["Power_Conumption"]/site_pi[0]["Generated_Power"]*100),0))+'%'
            print(str(utilization))
            context.update({

                "site_vendor": site_pi[0]["Site_Vendor"],
                "PowerConumption": site_pi[0]["Power_Conumption"],
                "Generated_Power": site_pi[0]["Generated_Power"],
                "utilization": utilization,
                "site_type": site_pi[0]["Site_Type"],
                "cabinets_type": site_pi[0]["Cabients_Type"],
                "Cabinet_num": site_pi[0]["Cabinet_Num"],
                "System_Voltage": site_pi[0]["System_Voltage"],
                "Power_Cabinet": site_pi[0]["Power_Cabinet"],
                "Rect_Count": site_pi[0]["Rect_Count"],
                "Battery_Type": site_pi[0]["Battery_Type"],
                "Bat_Count": site_pi[0]["Bat_Count"],

            })
        if civil_info.objects.filter(site_id=site).exists():
            existance = "yes"
            site_ci = civil_info.objects.filter(site_id=site).values()
            context.update({
                "RT_GF": site_ci[0]["RT_GF"],
                "st_type": site_ci[0]["ST_Type"],
                "height": site_ci[0]["Height"],
                "grillage": site_ci[0]["Grillage"],
                "anchoring": site_ci[0]["Anchoring"],
                "building": site_ci[0]["Building"],
                "new_requirement_details": site_ci[0]["new_requirement_details"],
                "project_name": site_ci[0]["Project_Name"],
                "site_status": site_ci[0]["Site_Status"],
                "Consultant_recommendations": site_ci[0]["Consultant_recommendations"],
                "remarks": site_ci[0]["Remarks"],
            })

        print(context)
        context.update({"site_search": existance})
    elif request.method == 'POST' and ("crq_update" in request.POST):
        start = time.time()

        myfile = request.FILES['myfile']
        print("start")
        df = read_excel(myfile)
        df = df.fillna('0')
        data = []
        for ind in df.index:
            record = power_info(
                Site_Name=df["Site_Name"][ind],
                site_id=df["site_id"][ind],
                Site_Vendor=df["Site_Vendor"][ind],
                Site_Region=df["Site_Region"][ind],
                Site_Type=df["Site_Type"][ind],
                Site_State=df["Site_State"][ind],
                Position=df["Position"][ind],
                Governate=df["Governate"][ind],
                Cabients_Type=df["Cabients_Type"][ind],
                Cabinet_Num=df["Cabinet_Num"][ind],
                Cabinet_Activity=df["Cabinet_Activity"][ind],
                System_Voltage=df["System_Voltage"][ind],
                Rectifier_Type=df["Rectifier_Type"][ind],
                Rect_Count=df["Rect_Count"][ind],
                Needed_Rectifiers=df["Needed_Rectifiers"][ind],
                Battery_Type=df["Battery_Type"][ind],
                Bat_Count=df["Bat_Count"][ind],
                Needed_Batteries=df["Needed_Batteries"][ind],
                Power_Cabinet=df["Power_Cabinet"][ind],
                Power_Conumption=df["Power_Conumption"][ind],
                Generated_Power=df["Generated_Power"][ind],
                FC_Comp_Name=df["FC_Comp_Name"][ind],
                FC_Comp_Count=df["FC_Comp_Count"][ind],
                Battery_cabinet=df["Battery_cabinet"][ind],
                Bat_Cab_Count=df["Bat_Cab_Count"][ind],
            )
            data.append(record)
        power_info.objects.filter(all).delete()
        power_info.objects.bulk_create(data)
        duration = time.time() - start
        print(duration)
        context = {"admin_risk_msg": "submit"}
        print(context)
    return render(request, "site_history/site_history_new.html", context)



# ------old authentication-------
# def auth_privillage(user_id):
#     dict={}
#     if Super_User.objects.filter(user_id=user_id).exists():
#         dict.update({"usertype":"Super_user","rw":"Read_write"})
#         print(dict)
#     elif HOD.objects.filter(user_id=user_id).exists():
#         dict.update({"usertype":"HOD","rw":"Read"})
#     elif User.objects.filter(user_id=user_id).exists():
#         dict.update({"usertype":"user","rw":"Read"})
#     elif Manager.objects.filter(user_id=user_id).exists():
#         dict.update({"usertype":"user","rw":"Read"})
#     elif SPOC.objects.filter(user_id=user_id).exists():
#         dict.update({"usertype":"spoc","rw":"Read_write"})
#         print(dict)
#     else:
#         dict.update({"usertype": "not_auth", "rw": "Read_write"})
#         print("user doesn't have privillage")
#
#     return dict