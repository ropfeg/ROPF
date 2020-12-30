from django.shortcuts import render,redirect
import pandas as pd
import time
import glob
import os
from shutil import copyfile
from ropf_auth.models import user_privilege,UserProfile
from .NFM_RCA_V4 import add_physical_technology,add_site_power_source,\
    add_site_unified_power_source,add_backup_problem_ods,add_guard,add_north_sinai,cust_RC
from django.contrib.auth.decorators import login_required
from datetime import datetime
from servant_app.models import general_info




# Create your views here.
@login_required(login_url='/')
def nfm_rca(request):
    context={}
    user_name = request.user.username
    user_id = request.user.id
    # print(user_id)
    context = {"username":user_name}
    # --------- start auth ------------
    if user_privilege.objects.filter(user_id=user_id).exists():

        if user_privilege.objects.get(user_id=user_id).rca_nfm == "no":
            return redirect("/auth_error/")
        else:
            context.update({
                'userprivileges':user_privilege.objects.get(user_id=user_id).rca_nfm,
                'read': ['r', 'cr','cru', 'crud'],
                'read_write': ['cr', 'cru','crud'],
                'cru':['cru', 'crud'],
                'crud':['crud']
            })
    if UserProfile.objects.filter(user_id=user_id).exists():

        userprofile = UserProfile.objects.get(user_id=user_id)
        print(userprofile)
        # print(userprofile.image.url)
        context.update({
                    # "avatar":userprofile.image.url

        })

    # ----------- end auth ------------

    #------------ update template links
    context.update({"gaurd_list_temp":"../static/NFM_RCA/NFM_RCA_Templates/guarded_sites.xlsx",
                    "uni_power_src_temp":"../static/NFM_RCA/NFM_RCA_Templates/unified_power_source.xlsx",
                    "raw_data_temp":"../static/NFM_RCA/NFM_RCA_Templates/raw_data_temp.xlsx",
                    "backup_time_temp":"../static/NFM_RCA/NFM_RCA_Templates/backup_time_temp.xlsx",

                    })
    # NFM_RCA_files = glob.glob('./static/NFM_RCA/NFM_RCA_Result*')  # * means all if need specific format then *.csv
    # latest_NFM_RCA = max(NFM_RCA_files, key=os.path.getctime)
    # print(latest_NFM_RCA)
    # SM_RCA_files = glob.glob('./static/NFM_RCA/SM_RCA_Result*')  # * means all if need specific format then *.csv
    # latest_SM_RCA = max(SM_RCA_files, key=os.path.getctime)
    # print(latest_SM_RCA)
    # missing_criteria_RCA_files = glob.glob('./static/NFM_RCA/missing_criteria_RCA_Result_*')  # * means all if need specific format then *.csv
    # latest_missing_criteria_RCA = max(missing_criteria_RCA_files, key=os.path.getctime)
    # print(latest_SM_RCA)
    # context.update({"last_modified_nfm":"."+latest_NFM_RCA,"last_modified_sm":"."+latest_SM_RCA,
    #                 "missing_criteria":"."+latest_missing_criteria_RCA,"last_date":latest_NFM_RCA[32:48]})
    if request.method == 'POST' and ("Start_prep" in request.POST):
        raw_data = request.FILES['raw_data']
        back_up_time= request.FILES['back_up_time']
        # gaurd_list = request.FILES['gaurd_list']
        # north_sinai = request.FILES['north_sinai']
        # unified_pwr = request.FILES['unified_pwr']
        gaurd_list="./static/NFM_RCA/NFM_RCA_DB/guarded_sites.xlsx"
        north_sinai="./static/NFM_RCA/NFM_RCA_DB/north_sinai_sites.xlsx"
        unified_pwr="./static/NFM_RCA/NFM_RCA_DB/unified_power_source.xlsx"
        start = time.time()
        df_raw_data = pd.read_excel(raw_data)
        try:
            add_physical_technology(df_raw_data, "Asset Id")
            df_raw_data["Phy Site"] = df_raw_data["Phy Site"].apply(pd.to_numeric, errors='coerce').fillna(df_raw_data["Phy Site"])
            df_raw_data = add_site_unified_power_source(df_raw_data,unified_pwr)
            df_raw_data = add_guard(df_raw_data,gaurd_list)
            df_raw_data = add_north_sinai(df_raw_data,north_sinai)
            df_raw_data = add_backup_problem_ods(df_raw_data,back_up_time)
            df_raw_data = cust_RC(df_raw_data)


            missing_criteria_df=df_raw_data.loc[(df_raw_data["customized RC1 Tier 1"]=="N/A")|
                                            (df_raw_data["customized RC1 Tier 1"] == "Multiple" )|
                                            (df_raw_data["customized RC1 Tier 1"].isnull())
                                            ]




            SM_df = pd.DataFrame()
            SM_df = df_raw_data[
                ['Ref No', 'Incident Number', 'Asset Id', 'Total Loss', 'Phy Site', 'Technology', 'Radio Region',
                 'North Sinai',
                 'customized RC1 Tier 1', 'customized RC1 Tier 2', 'customized RC1 Tier 3']]
            now = datetime.now()
            # date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
            date_time =''
            df_raw_data.to_excel("./static/NFM_RCA/NFM_RCA_Result_"+date_time+".xlsx")

            SM_df.to_excel("./static/NFM_RCA/SM_RCA_Result_"+date_time+".xlsx")
            missing_criteria_df.to_excel("./static/NFM_RCA/missing_criteria_RCA_Result_"+date_time+".xlsx")
            context.update({"code":"success",
                            "last_modified_nfm": "../static/NFM_RCA/NFM_RCA_Result_"+date_time+".xlsx",
                            "last_modified_sm": "../static/NFM_RCA/SM_RCA_Result_" + date_time+".xlsx",
                            "missing_criteria":"../static/NFM_RCA/missing_criteria_RCA_Result_"+date_time+".xlsx"})
            end = time.time()


            print(start - end)
            print(context)
        except KeyError:
            context.update({"sheet_name":"not_exist"})
        return render(request, 'nfm_crca.html', context)
    elif request.method == 'POST' and ("update_crcdb" in request.POST):
        try:
            if "unified_pwr" in request.FILES:
                unified_pwr=request.FILES['unified_pwr']
                df_unified_pwr = pd.read_excel(unified_pwr)
                for ind in df_unified_pwr.index:
                    general_info.objects.filter(site_id=df_unified_pwr["Physical Site"][ind]).update(
                        power_source_status=df_unified_pwr["Final Feedback"][ind],
                        )
                    print("power_source_add")
                copyfile(unified_pwr, "./static/NFM_RCA/NFM_RCA_DB/unified_power_source.xlsx")
            if "north_sinai" in request.FILES:
                north_sinai = request.FILES['north_sinai']
                df_north_sinai = pd.read_excel(north_sinai)
                for ind in df_north_sinai.index:
                    if general_info.objects.filter(site_id=df_north_sinai["Site ID"][ind]).exists():
                        print(df_north_sinai["Site ID"][ind])
                        general_info.objects.filter(site_id=df_north_sinai["Site ID"][ind]).update(
                            north_sinai_status="yes",
                        )

                copyfile(north_sinai, "./static/NFM_RCA/NFM_RCA_DB/north_sinai_sites.xlsx")
            if "gaurd_list" in request.FILES:
                gaurd_list=request.FILES['gaurd_list']
                df_gaurd_list = pd.read_excel(gaurd_list)
                for ind in df_gaurd_list.index:
                    if general_info.objects.filter(site_id=df_gaurd_list["Site ID"][ind]).exists():
                        print(df_gaurd_list["Site ID"][ind])
                        general_info.objects.filter(site_id=df_gaurd_list["Site ID"][ind]).update(
                            guarded_status="yes",
                        )
                copyfile(gaurd_list, "./static/NFM_RCA/NFM_RCA_DB/guarded_sites.xlsx")
        except KeyError:
            context.update({"sheet_name":"not_exist"})
        return render(request, 'nfm_crca.html', context)
    print(context)
    return render(request, 'nfm_crca.html', context)