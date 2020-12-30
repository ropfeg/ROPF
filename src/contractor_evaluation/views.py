from django.shortcuts import render
from django.shortcuts import render,redirect
from pandas import read_excel
import time
import glob
import os
from shutil import copyfile
from ropf_auth.models import user_privilege,UserProfile
from .models import Contractor_DB,rollout_pool,rollout_db,telecom_civil_db,Ranking_db,RankTabCivil\
    ,RankingTab_Telecom,RankingTabPower,FinalTab_Civil

from django.contrib.auth.decorators import login_required
from datetime import datetime
from servant_app.models import general_info
# Create your views here.
from fiscalyear import *
import fiscalyear
from django.db.models import Sum, Q

def vodfone_fy(c):

    fiscalyear.setup_fiscal_calendar(start_month=4)
    fiscalyear.setup_fiscal_calendar(start_day=10)

    return (str(c.year - 2000) + '/' + str(c.fiscal_year - 2000))

def vodfone_quarter(c):
    fiscalyear.setup_fiscal_calendar(start_month=4)
    fiscalyear.setup_fiscal_calendar(start_day=10)

    return ('Q' + str(c.quarter))
def contractor_db_update(back_up_time):
    contractor_df = read_excel(back_up_time)
    contractor_df = contractor_df.replace({"Yes": True, "No": False})
    for ind in contractor_df.index:
        Contractor_DB.objects.create(
            Contractor_Name=contractor_df["Contractor Name"][ind],
            Existing=contractor_df["Existing"][ind],
            Civil=contractor_df["Civil"][ind],
            Civil_Active=contractor_df["CivilActive"][ind],
            Telecom=contractor_df["Telecom"][ind],
            Telecom_Active=contractor_df["TelecomActive"][ind],
            Civil_Enhancement=contractor_df["Civil_Enhancement"][ind],
            Civil_Enhancement_Active=contractor_df["Civil_Enhancement_Active"][ind],

        )

def telecom_civil_db_update(df):
    for ind in df.index:
        print(df["Contractor"][ind])
        telecom_civil_db.objects.create(
            Contractor=Contractor_DB.objects.get(Contractor_Name=df["Contractor"][ind]),
            region=df["Region"][ind],
            Quarter=vodfone_quarter(FiscalDate.today()),
            Current_FY=vodfone_fy(FiscalDate.today()),
            CivilupgradesTarget=df["CivilupgradesTarget"][ind],
            CivilupgradesAchieved=df["CivilupgradesAchieved"][ind],
            Civilupgrades_Comment=df["Civilupgrades_Comments"][ind],
            TelecomServicesTarget=df["TelecomServicesTarget"][ind],
            TelecomservicesAchieved=df["TelecomservicesAchieved"][ind],
            Telecomservices_Comment=df["Telecomservices_Comment"][ind],
            Civilenhancementactivities_Target=df["Civilenhancementactivities_Target"][ind],
            Civilenhancementactivities_Achieved=df["Civilenhancementactivities_Achieved"][ind],
            Civilenhancementactivities_comment=df["Civilenhancementactivities_comment"][ind],
        )

        # telecom_civil_db.objects.filter(Current_FY=vodfone_fy(FiscalDate.today()), Contractor=2014).aggregate(Sum('num_pages'))
@login_required(login_url='/')
def cont_eva(request):
    context = {}

    c = FiscalDate.today()
    print(c)
    print(vodfone_fy(c))

    user_name = request.user.username
    user_id = request.user.id
    # print(user_id)
    context = {"username": user_name}
    # --------- start auth ------------
    if user_privilege.objects.filter(user_id=user_id).exists():

        if user_privilege.objects.get(user_id=user_id).rca_nfm == "no":
            return redirect("/auth_error/")
        else:
            context.update({
                'userprivileges': user_privilege.objects.get(user_id=user_id).contractor_evaluation,
                'read': ['r', 'cr', 'cru', 'crud'],
                'read_write': ['cr', 'cru', 'crud'],
                'cru': ['cru', 'crud'],
                'crud': ['crud']
            })
    if UserProfile.objects.filter(user_id=user_id).exists():
        userprofile = UserProfile.objects.get(user_id=user_id)
        print(userprofile)
        # print(userprofile.image.url)
        context.update({
            # "avatar":userprofile.image.url

        })

    # ----------- end auth ------------
    # print(Contractor_DB.objects.all().values_list('Contractor_Name', flat=True))
    for contractor in Contractor_DB.objects.all().values_list('Contractor_Name', flat=True):
        print(Contractor_DB.objects.get(Contractor_Name=contractor).Contractor_Name)

        sum=telecom_civil_db.objects.filter(Current_FY=vodfone_fy(FiscalDate.today()), Contractor=Contractor_DB.objects.get(Contractor_Name=contractor)).aggregate(
            Sum('CivilupgradesTarget'))

        print(sum['CivilupgradesTarget__sum'])


    # if request.method == 'POST' and ("Start_prep" in request.POST):
    #     raw_data = request.FILES['raw_data']
    #     back_up_time= request.FILES['back_up_time']
    #     # print(Contractor_DB.objects.get(Contractor_Name="Alkan").id)
    #     df = read_excel(raw_data)
    #     # update upgrade database DB4
    #
    #
    #
    #
    return render(request, 'cont_eva.html', context)