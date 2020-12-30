from django.shortcuts import render,redirect
from .models import site_management_db,cluster_average
from servant_app.models import general_info,tx_info,radio_info
from site_history_app.models import power_info,civil_info
from pandas import read_excel,Timestamp
import time
from django.contrib.auth.decorators import login_required
from ropf_auth.models import user_privilege,UserProfile
# Create your views here.

@login_required(login_url='/')
def contract_renegotiation(request):

    user_name = request.user.username
    user_id = request.user.id
    # print(user_id)
    context = {"username":user_name}
    # --------- start auth ------------
    if user_privilege.objects.filter(user_id=user_id).exists():

        if user_privilege.objects.get(user_id=user_id).contract_renegotiation == "no":
            return redirect("/auth_error/")
        else:
            context.update({
                'userprivileges':user_privilege.objects.get(user_id=user_id).contract_renegotiation,
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
                    "user_region": userprofile.user_region,
                    # "avatar":userprofile.image.url

        })
    # ----------- end auth ------------


    if request.method == 'POST' and ("single_search" in request.POST):
        dict = {
            "Critical": 0.13,
            "High": 0.1,
            "Medium": 0.08,
            "Low": 0.05,
            "Very Low": 0.05,
            "Not Ranked": 0.05

        }
        site = request.POST.get("site_id")
        print(site)
        existance="submit"
        if general_info.objects.filter(site_id=site).exists():
            existance = "yes"
            site_gi = general_info.objects.filter(site_id=site).values()
            # ------------   Start Region _authentication --------------
            if context["user_region"] in [site_gi[0]["region"],"All"]:
                pass
            else:
                context.update({"region_search_msg":"incorrect"})
                return render(request, "site_management/contract_renegotiation.html", context)
            # ------------   End Region _authentication --------------
            context.update({
                "site_id": site,
                "option": site_gi[0]["option"],
                "region": site_gi[0]["region"],
                "sub_region": site_gi[0]["sub_region"],
                "structure_type": site_gi[0]["structure_type"],
                "site_type": site_gi[0]["site_type"],
            })
            context["map"] = "https://maps.google.com/maps?q=" + str(site_gi[0]["latitude"]) + "%2C" + str(site_gi[0]["longitude"]) + "&t=k&z=15&ie=UTF8&iwloc=&output=embed"
        if radio_info.objects.filter(site_id=site).exists():
            existance = "yes"
            site_ri = radio_info.objects.filter(site_id=site).values()
            context.update({

                "rank": site_ri[0]["rank"],
            })
        if tx_info.objects.filter(site_id=site).exists():
            existance = "yes"
            site_txi = tx_info.objects.filter(site_id=site).values()
            context.update({

                "cascaded_sites": site_txi[0]["cascaded_sites"],
            })
        if cluster_average.objects.filter(site_id=site).exists():
            existance = "yes"
            site_cl = cluster_average.objects.filter(site_id=site).values()
            context.update({

                "cl_avg_rent": site_cl[0]["cl_avg_rent"],
            })
        if site_management_db.objects.filter(site_id=site).exists():
            existance = "yes"
            site_smd=site_management_db.objects.filter(site_id=site).values()
            expected_payment=round( site_smd[0]["Last_Rent"] * (1 + dict[site_ri[0]["rank"]]),2)
            print(site_smd[0])
            context.update({
                "System_Start_Date":site_smd[0]["System_Start_Date"],
                "System_End_Date":site_smd[0]["System_End_Date"],
                "Calc_From":site_smd[0]["Calc_From"],
                "Calc_To":site_smd[0]["Calc_To"],
                "Last_Rent": site_smd[0]["Last_Rent"],
                "Expected_Payment": expected_payment,
            })
        context.update({"risk_msg": existance})
    elif request.method == 'POST' and ("sm_update" in request.POST):
        start=time.time()
        myfile = request.FILES['myfile']
        print("start")
        df = read_excel(myfile)
        df[['System_Start_Date', 'System_End_Date','Calc_From','Calc_To']] = df[['System_Start_Date', 'System_End_Date','Calc_From','Calc_To']].fillna(Timestamp('19900101'))
        df=df.fillna('0')
        data = []
        for ind in df.index:
            record=site_management_db(
                site_id=df["site_id"][ind],
                Last_Rent=df["Last_Rent"][ind],
                System_Start_Date=df["System_Start_Date"][ind],
                System_End_Date=df["System_End_Date"][ind],
                Calc_From=df["Calc_From"][ind],
                Calc_To=df["Calc_To"][ind],
                Access_Status=df["Access_Status"][ind],
                problematic_owner=df["problematic_owner"][ind],
                health_safety=df["health_safety"][ind],
                tech_issue=df["tech_issue"][ind],
                remove_order=df["remove_order"][ind],
                legal=df["legal"][ind],
            )
            data.append(record)
        site_management_db.objects.bulk_create(data)
        duration=time.time()-start
        print(duration)
        context = {"risk_msg": "submit"}
    elif request.method == 'POST' and ("ca_update" in request.POST):
        start=time.time()
        myfile = request.FILES['myfile']
        print("start")
        df = read_excel(myfile)
        df=df.fillna('0')
        data = []
        for ind in df.index:
            record=cluster_average(
                site_id=df["site_id"][ind],
                cl_avg_key=df["cl_avg_key"][ind],
                cl_avg_rent=df["cl_avg_rent"][ind],
            )
            data.append(record)
        cluster_average.objects.bulk_create(data)
        duration=time.time()-start
        print(duration)
        context = {"admin_risk_msg": "submit"}
    elif request.method == 'POST' and ("gi_update" in request.POST):
        start=time.time()
        myfile = request.FILES['myfile']
        print("start")
        df = read_excel(myfile)

        df=df.fillna('0')
        data = []
        for ind in df.index:
            record=general_info(
                site_id=df["site_id"][ind],
                option=df["option"][ind],
                region=df["region"][ind],
                sub_region=df["sub_region"][ind],
                longitude=df["longitude"][ind],
                latitude=df["latitude"][ind],
                site_type=df["site_type"][ind],
                structure_type=df["structure_type"][ind],
            )
            data.append(record)
        general_info.objects.bulk_create(data)
        duration=time.time()-start
        print(duration)
        context = {"admin_risk_msg": "submit"}
    elif request.method == 'POST' and ("ri_update" in request.POST):
        start = time.time()
        myfile = request.FILES['myfile']
        print("start")
        df = read_excel(myfile)

        df = df.fillna('0')
        data = []
        for ind in df.index:
            record = radio_info(
                site_id=df["site_id"][ind],
                rank=df["rank"][ind],
            )
            data.append(record)
        radio_info.objects.bulk_create(data)
        duration = time.time() - start
        print(duration)
        context = {"risk_msg": "submit"}
    elif request.method == 'POST' and ("ti_update" in request.POST):
        start = time.time()
        myfile = request.FILES['myfile']
        print("start")
        df = read_excel(myfile)

        df = df.fillna('None')
        data = []
        for ind in df.index:
            record = tx_info(
                site_id=df["site_id"][ind],
                cascaded_sites=df["cascaded_sites"][ind],
            )
            data.append(record)
        tx_info.objects.bulk_create(data)
        duration = time.time() - start
        print(duration)
        context = {"admin_risk_msg": "submit"}




    elif request.method == 'POST' and ("delete" in request.POST):
        start = time.time()
        tx_info.objects.all().delete()
        duration = time.time() - start
        print(duration)

    return render(request, "site_management/contract_renegotiation.html", context)




@login_required(login_url='/')
def site_continuity_risk(request):
    user_name = request.user.username
    user_id = request.user.id
    # print(user_id)
    context = {"username": user_name}
    # --------- start auth ------------
    if user_privilege.objects.filter(user_id=user_id).exists():
        if user_privilege.objects.get(user_id=user_id).site_continuity_risk == "no":
            return redirect("/auth_error/")
        else:
            context.update({
                'userprivileges': user_privilege.objects.get(user_id=user_id).site_continuity_risk,
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
            # "avatar": userprofile.image.url,
            "user_region":userprofile.user_region,

        })
    # ----------- end auth ------------
    if request.method == 'POST' and ("single_search" in request.POST):
        dict = {
            "Critical": 0.13,
            "High": 0.1,
            "Medium": 0.08,
            "Low": 0.05,
            "Very Low": 0.05,
            "Not Ranked": 0.05

        }
        site = request.POST.get("site_id")
        print(site)
        existance="submit"
        if general_info.objects.filter(site_id=site).exists():

            existance = "yes"
            site_gi = general_info.objects.filter(site_id=site).values()
            # ------------   Start Region _authentication --------------
            if context["user_region"] in [site_gi[0]["region"],"All"]:
                pass
            else:
                context.update({"region_search_msg":"incorrect"})
                return render(request, "site_management/site_continuity_risk.html", context)
            # ------------   End Region _authentication --------------
            context.update({
                "site_id": site,
                "option": site_gi[0]["option"],
                "region": site_gi[0]["region"],
                "sub_region": site_gi[0]["sub_region"],
                "structure_type": site_gi[0]["structure_type"],
                "site_type": site_gi[0]["site_type"],
            })
            context["map"] = "https://maps.google.com/maps?q=" + str(site_gi[0]["latitude"]) + "%2C" + str(site_gi[0]["longitude"]) + "&t=k&z=15&ie=UTF8&iwloc=&output=embed"
        if radio_info.objects.filter(site_id=site).exists():
            existance = "yes"
            site_ri = radio_info.objects.filter(site_id=site).values()
            context.update({

                "rank": site_ri[0]["rank"],
            })
        if tx_info.objects.filter(site_id=site).exists():
            existance = "yes"
            site_txi = tx_info.objects.filter(site_id=site).values()
            context.update({

                "cascaded_sites": site_txi[0]["cascaded_sites"],
            })
        if cluster_average.objects.filter(site_id=site).exists():
            existance = "yes"
            site_cl = cluster_average.objects.filter(site_id=site).values()
            context.update({

                "cl_avg_rent": site_cl[0]["cl_avg_rent"],
            })
        if site_management_db.objects.filter(site_id=site).exists():
            existance = "yes"
            site_smd=site_management_db.objects.filter(site_id=site).values()
            expected_payment=round( site_smd[0]["Last_Rent"] * (1 + dict[site_ri[0]["rank"]]),2)
            print(context)
            context.update({
                "access_status": site_smd[0]["Access_Status"],
                "problematic_owner": site_smd[0]["problematic_owner"],
                "h_s": site_smd[0]["health_safety"],
                "tech_issue": site_smd[0]["tech_issue"],
                "remove_order":site_smd[0]["remove_order"],
                "legal":site_smd[0]["legal"],
                "System_End_Date":site_smd[0]["System_End_Date"],
                "Calc_To":site_smd[0]["Calc_To"],
                "Last_Rent": site_smd[0]["Last_Rent"],

            })
        context.update({"risk_msg": existance})

    elif request.method == 'POST' and ("sm_update" in request.POST):
        start=time.time()
        myfile = request.FILES['myfile']
        print("start")
        df = read_excel(myfile)
        df[['System_Start_Date', 'System_End_Date','Calc_From','Calc_To']] = df[['System_Start_Date', 'System_End_Date','Calc_From','Calc_To']].fillna(Timestamp('19900101'))
        df=df.fillna('0')
        data = []
        for ind in df.index:
            record=site_management_db(
                site_id=df["site_id"][ind],
                Last_Rent=df["Last_Rent"][ind],
                System_Start_Date=df["System_Start_Date"][ind],
                System_End_Date=df["System_End_Date"][ind],
                Calc_From=df["Calc_From"][ind],
                Calc_To=df["Calc_To"][ind],
                Access_Status=df["Access_Status"][ind],
                problematic_owner=df["problematic_owner"][ind],
                health_safety=df["health_safety"][ind],
                tech_issue=df["tech_issue"][ind],
                remove_order=df["remove_order"][ind],
                legal=df["legal"][ind],
            )
            data.append(record)
        site_management_db.objects.bulk_create(data)
        duration=time.time()-start
        print(duration)
        context = {"admin_risk_msg": "submit"}

    return render(request, "site_management/site_continuity_risk.html", context)



