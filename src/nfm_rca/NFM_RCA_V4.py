import pandas as pd
import time
def containsAny(str, set):
    """Check whether 'str' contains ANY of the chars in 'set'"""
    return 1 in [c in str for c in set]
def add_physical_technology(file,site_column_name):
    #extract the physical ID
    char=['c','g','l','m','h']
    # site_column_name="Asset Id"
    wcdma_list=['g','m']
    lte_list=['l']
    physical=[]
    technology=[]
    for site_id in range(len(file[site_column_name])):
        string=str(file[site_column_name][site_id]).lower()
        if containsAny(string ,char):
            physical.append(file[site_column_name][site_id][1:])
        else:
            physical.append(str(file[site_column_name][site_id])[:])
        if containsAny(string ,wcdma_list):
            technology.append("3G")
        elif containsAny(string ,lte_list):
            technology.append("4G")
        else:
            technology.append("2G")
    file["Phy Site"]=physical
    file["Technology"] = technology
def add_site_power_source(file,gen_list): # with Generator list only
    power_source=pd.read_excel(gen_list)
    power_source["Phy Site"] = power_source["Asset ID"]
    power_source["Site Power Source"]=power_source["Power Team FB"]
    power_source = power_source[['Phy Site', 'Site Power Source']]
    print(power_source.head())
    file=pd.merge(file, power_source,how='left', on='Phy Site')
    file["Site Power Source"]=file["Site Power Source"].fillna("Commercial")
    return file
def add_site_unified_power_source(file,unified_list): # with Unified power source
    power_source=pd.read_excel(unified_list)
    power_source["Phy Site"] = power_source["Physical Site"]
    power_source["Site Power Source"]=power_source["Final Feedback"]
    power_source["Radio Region"] = power_source["Final Region"]
    power_source = power_source[['Phy Site', 'Site Power Source',"Radio Region"]]
    print(power_source.head())
    file=pd.merge(file, power_source,how='left', on='Phy Site')
    # file["Site Power Source"]=file["Site Power Source"].fillna("Commercial")
    return file
def add_backup_problem_ods(file,backup_list):
    bkup = pd.read_excel(backup_list)
    add_physical_technology(bkup,"Asset ID")
    bkup=bkup.sort_values(by=['Last Modified Date'], ascending=False)
    bkup=bkup.drop_duplicates(subset=['Phy Site'], keep='first')
    bkup_dict={"Resolved":"pending","Pending":"Yes","Assigned":"Yes",}

    bkup["backup problem"]=bkup["Status*"].map(bkup_dict,na_action='ignore')
    bkup.loc[(bkup["Assigned Support Company"] == 'Regional Operations') &(bkup["backup problem"] == "pending"),'backup problem']= 'No'

    bkup.loc[(bkup["Assigned Support Company"] != 'Regional Operations')& (bkup["backup problem"] == "pending"), 'backup problem'] = 'Yes'

    bkup.loc[(bkup["Assigned Support Company"] == 'Regional Operations') & (bkup["backup problem"] == "pending") , 'backup problem'] = 'No'
    bkup.to_excel("bckup_result_test.xlsx")
    bkup = bkup[['Phy Site', "backup problem",'Last Modified Date','Incident ID*+']]
    bkup.to_excel("bckup_result.xlsx")
    file = pd.merge(file, bkup, how='left', on='Phy Site')
    return file

def add_guard(file,guard_list):
    guard = pd.read_excel(guard_list)
    guard["Phy Site"] = guard["Site ID"]
    guard["Site Guarded"] = "Site Guarded"
    guard = guard[['Phy Site', 'Site Guarded']]
    print(guard.head())
    file = pd.merge(file, guard, how='left', on='Phy Site')
    file["Site Guarded"] = file["Site Guarded"].fillna("Not guarded")
    return file


def add_north_sinai(file,north_list):
    guard = pd.read_excel(north_list)
    guard["Phy Site"] = guard["Site ID"]
    guard = guard[['Phy Site', 'North Sinai']]
    print(guard.head())
    file = pd.merge(file, guard, how='left', on='Phy Site')
    file["North Sinai"] = file["North Sinai"].fillna("No")
    return file


def cust_RC(file):
    file["customized RC1 Tier 1"] = "N/A"
    file["customized RC1 Tier 2"] = "N/A"
    file["customized RC1 Tier 3"] = "N/A"
    # "Root Cause1 Tier 1"
    # "Root Cause1 Tier 2"
    # "Root Cause1 Tier 3"
    # "Root Cause2 Tier 1"
    # "Root Cause2 Tier 2"
    # "Root Cause2 Tier 3"
    # "Root Cause3 Tier 1"
    # "Root Cause3 Tier 2"
    # "Root Cause3 Tier 3"
    # # "Categorization Tier 1"
    # free_rc_mapping_Tier1={
    #     "Field Tx node":"TX Access","VF Core TX problem":"TX Backhaul","Environmental":"Environmental",
    #     "Power":"Power","Telecom":"Telecom Problem","TE Core Tx problem":"TX Backhaul",
    #     "Microwave":"TX Access","Generator":"Power","VF Core Tx Problem":"TX Backhaul",
    #     "Performance Problem":"Telecom Problem","Radio":"Telecom Problem","Solar Power":"Power",
    #     }
    # free_rc_mapping_Tier2 = {
    #         "Field Tx node": "TX Access Automated Resolution", "VF Core TX problem": "TX Backhaul Automated Resolution",
    #         "Environmental": "Environmental Automated Resolution","Power": "Power Automated Resolution",
    #         "Telecom": "Telecom Problem Automated Resolution", "TE Core Tx problem": "TX Backhaul Automated Resolution",
    #         "Microwave": "TX Access Automated Resolution","VF Core Tx Problem":"TX Backhaul Automated Resolution",
    #         "Generator": "Generator Automated Resolution","Performance Problem": "Performance Problem Automated Resolution",
    #          "Radio": "Telecom Problem Automated Resolution","Solar Power": "Solar Power Automated Resolution",
    #     }
    # free_rc_mapping_Tier3 = {
    #         "Field Tx node": "TX Access Automated Resolution", "VF Core TX problem": "TX Backhaul Automated Resolution",
    #         "Environmental": "Environmental Automatic Resolution","Power": "Power Automated Resolution",
    #         "Telecom": "Telecom Problem Automated Resolution", "TE Core Tx problem": "Transmission TE Automated Resolution",
    #         "Microwave": "TX Access Automated Resolution","VF Core Tx Problem":"TX Fluctuation Automatic Resolution",
    #         "Generator": "Generator Automated Resolution","Performance Problem": "Performance Problem Automated Resolution",
    #          "Radio": "Telecom Problem Automated Resolution","Solar Power": "Solar Power Automated Resolution",
    #
    # }
    # file["customized RC1 Tier 1"]="N/A"
    # file["customized RC1 Tier 2"]="N/A"
    # file["customized RC1 Tier 3"]="N/A"
    # file.loc[(file["Root Cause1 Tier 3"].isnull())&
    #             (file["Root Cause2 Tier 3"].isnull()) &
    #             (file["Root Cause3 Tier 3"].isnull())
    #             , 'customized RC1 Tier 1']= file.loc[(file["Root Cause1 Tier 3"].isnull())&
    #                                                 (file["Root Cause2 Tier 3"].isnull()) &
    #                                                 (file["Root Cause3 Tier 3"].isnull())
    #                                                 ,"Categorization Tier 1"].map(free_rc_mapping_Tier1,na_action='ignore')
    #
    # file.loc[(file["Root Cause1 Tier 3"].isnull()) &
    #          (file["Root Cause2 Tier 3"].isnull()) &
    #          (file["Root Cause3 Tier 3"].isnull())
    #         , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 3"].isnull()) &
    #                                       (file["Root Cause2 Tier 3"].isnull()) &
    #                                       (file["Root Cause3 Tier 3"].isnull())
    #                                         , "Categorization Tier 1"].map(free_rc_mapping_Tier2, na_action='ignore')
    # file.loc[(file["Root Cause1 Tier 3"].isnull()) &
    #          (file["Root Cause2 Tier 3"].isnull()) &
    #          (file["Root Cause3 Tier 3"].isnull())
    #         , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 3"].isnull()) &
    #                                       (file["Root Cause2 Tier 3"].isnull()) &
    #                                       (file["Root Cause3 Tier 3"].isnull())
    #                                         , "Categorization Tier 1"].map(free_rc_mapping_Tier3, na_action='ignore')

    # -----------------------------------------------------------------------------------------------------
    #------------------------------------------------ SM Case A -------------------------------------------
    sm_list=["Site Management Alex","Site Management Cairo","Site Management Delta","Site Management Giza",
             "Site Management Upper-Red Sea&Sinai Region"]
    file.loc[
             # ((file["Root Cause1 Tier 1"]!="Access & Vandalism") &
             # (file["Root Cause2 Tier 1"]!="Access & Vandalism") &
             # (file["Root Cause3 Tier 1"]!="Access & Vandalism"))&
             # (file["Site Guarded"] =="Not guarded") &
             (file["Support Group"].isin(sm_list))&
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] ="Access & Vandalism"
    file.loc[
             # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
             # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
             # (file["Root Cause3 Tier 1"] != "Access & Vandalism") )&
             # (file["Site Guarded"] == "Not guarded") &
             (file["Support Group"].isin(sm_list))&
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "Site management"
    file.loc[
             # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
             # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
             # (file["Root Cause3 Tier 1"] != "Access & Vandalism") )&
             # # (file["Site Guarded"] == "Not guarded") &
             (file["Support Group"].isin(sm_list))&
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "Owner Problem"
    # ------------------------------------------------ SM Case B -------------------------------------------
    # file.loc[
    #          # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
    #          # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
    #          # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
    #          # (file["Site Guarded"] == "Site Guarded") &
    #          (file["Support Group"].isin(sm_list))&
    #          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    # , 'customized RC1 Tier 1'] = "Access & Vandalism"
    # file.loc[
    #          # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
    #          # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
    #          # (file["Root Cause3 Tier 1"] != "Access & Vandalism") )&
    #          # (file["Site Guarded"] == "Site Guarded") &
    #          (file["Support Group"].isin(sm_list))&
    #          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    # , 'customized RC1 Tier 2'] = "Corporate Security"
    # file.loc[
    #          # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
    #          # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
    #          # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
    #          # (file["Site Guarded"] == "Site Guarded") &
    #          (file["Support Group"].isin(sm_list))&
    #          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    # , 'customized RC1 Tier 3'] = "BTS Corp Security"
    # ------------------------------ SM Case C
    # ------------------------------ BTS Corp Security case B
    # ------------------------------ CPC team Case B
    # ------------------------------ External Affairs Case B
    # ------------------------------ Mobile Resources Acquisition Case B
    # ------------------------------ Fixed Resources Acquisition Case B
    # ------------------------------ Health & Safety Management Case B


    access_vandalism_list =     ["Site Management Alex", "Site Management Cairo","Site Management Delta",
                                 "Site Management Giza","Site Management Upper-Red Sea&Sinai Region",
                                 "BTS Corp Security","CPC team","External Affairs","Mobile Resources Acquisition",
                                 "Fixed Resources Acquisition","Health & Safety Management","Site Sharing"
                                 ]
    Access_Vandalism_tier1={
                                "CPC":"Access & Vandalism",
                                "CPC team": "Access & Vandalism",
                                "Regulatory & governmental Problem": "Access & Vandalism",
                                "Owner Problem": "Access & Vandalism",
                                "Site Vandalism": "Access & Vandalism",
                                "Stealth Incident": "Access & Vandalism",
                                "BTS Corp Security": "Access & Vandalism",
                                "Site Sharing": "Sharing"

                            }
    Access_Vandalism_tier2 = {
        "CPC": "Account payable",
        "CPC team": "Account payable",
        "Regulatory & governmental Problem": "Regulatory & governmental",
        "Owner Problem": "Site Management",
        "Site Vandalism": "Corporate Security",
        "Stealth Incident": "Corporate Security",
        "BTS Corp Security": "Corporate Security",
        "Site Sharing": "Sharing Problems"
    }
    Access_Vandalism_tier3 = {
        "CPC": "CPC",
        "CPC team": "CPC",
        "Regulatory & governmental Problem": "External Affairs",
        "Owner Problem": "Owner Problem",
        "Site Vandalism": "BTS Corp Security",
        "Stealth Incident": "BTS Corp Security",
        "BTS Corp Security": "BTS Corp Security",
        "Site Sharing": "Access Problem"
    }
    # ------------------------------------  Tier 1
    file.loc[
             # (file["Root Cause1 Tier 1"] == "Access & Vandalism") &
             (file["Support Group"].isin(access_vandalism_list)) &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
                , 'customized RC1 Tier 1'] = file.loc[
                                            # (file["Root Cause1 Tier 1"] == "Access & Vandalism") &
                                            (file["Support Group"].isin(access_vandalism_list))&
                                            ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
                                             , "Support Group"].map(Access_Vandalism_tier1, na_action='ignore')
    file.loc[
             # (file["Root Cause2 Tier 1"] == "Access & Vandalism") &
             (file["Support Group"].isin(access_vandalism_list))&
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
            , 'customized RC1 Tier 1'] = file.loc[
                                             # (file["Root Cause2 Tier 1"] == "Access & Vandalism") &
                                             (file["Support Group"].isin(access_vandalism_list))&
                                            ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
                                            , "Support Group"].map(Access_Vandalism_tier1, na_action='ignore')
    file.loc[
             # (file["Root Cause3 Tier 1"] == "Access & Vandalism") &
             (file["Support Group"].isin(access_vandalism_list))&
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
            , 'customized RC1 Tier 1'] = file.loc[
                                            # (file["Root Cause3 Tier 1"] == "Access & Vandalism") &
                                            (file["Support Group"].isin(access_vandalism_list))&
                                            ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
                                            , "Support Group"].map(Access_Vandalism_tier1, na_action='ignore')

    # -------------------------------Tier 2

    file.loc[
             # (file["Root Cause1 Tier 1"] == "Access & Vandalism") &
             (file["Support Group"].isin(access_vandalism_list)) &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
            , 'customized RC1 Tier 2'] = file.loc[
                                          # (file["Root Cause1 Tier 1"] == "Access & Vandalism") &
                                          (file["Support Group"].isin(access_vandalism_list)) &
                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
                                          , "Support Group"].map(Access_Vandalism_tier2, na_action='ignore')
    file.loc[
             # (file["Root Cause2 Tier 1"] == "Access & Vandalism") &
             (file["Support Group"].isin(access_vandalism_list)) &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
            , 'customized RC1 Tier 2'] = file.loc[
                                          # (file["Root Cause2 Tier 1"] == "Access & Vandalism") &
                                          (file["Support Group"].isin(access_vandalism_list)) &
                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
                                          , "Support Group"].map(Access_Vandalism_tier2, na_action='ignore')
    file.loc[
             # (file["Root Cause3 Tier 1"] == "Access & Vandalism") &
             (file["Support Group"].isin(access_vandalism_list)) &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
            , 'customized RC1 Tier 2'] = file.loc[
                                          # (file["Root Cause3 Tier 1"] == "Access & Vandalism") &
                                          (file["Support Group"].isin(access_vandalism_list)) &
                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
                                          , "Support Group"].map(Access_Vandalism_tier2, na_action='ignore')
    # -------------------------------Tier 3
    file.loc[
             # (file["Root Cause1 Tier 1"] == "Access & Vandalism") &
             (file["Support Group"].isin(access_vandalism_list)) &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
             , 'customized RC1 Tier 3'] = file.loc[
                                          # (file["Root Cause1 Tier 1"] == "Access & Vandalism") &
                                          (file["Support Group"].isin(access_vandalism_list)) &
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
                                          , "Support Group"].map(Access_Vandalism_tier3, na_action='ignore')
    file.loc[
             # (file["Root Cause2 Tier 1"] == "Access & Vandalism") &
             (file["Support Group"].isin(access_vandalism_list)) &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
            , 'customized RC1 Tier 3'] = file.loc[
                                          # (file["Root Cause2 Tier 1"] == "Access & Vandalism") &
                                          (file["Support Group"].isin(access_vandalism_list)) &
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
                                          , "Support Group"].map(Access_Vandalism_tier3, na_action='ignore')
    file.loc[
            # (file["Root Cause3 Tier 1"] == "Access & Vandalism") &
             (file["Support Group"].isin(access_vandalism_list)) &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
             , 'customized RC1 Tier 3'] = file.loc[
                                          # (file["Root Cause3 Tier 1"] == "Access & Vandalism") &
                                          (file["Support Group"].isin(access_vandalism_list)) &
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
                                          , "Support Group"].map(Access_Vandalism_tier3, na_action='ignore')




    # -------------------------------------------- BTS Corp Security Case A ----------------------------------------------------
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"]=="BTS Corp Security") &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Access & Vandalism"
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"]=="BTS Corp Security") &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
             , 'customized RC1 Tier 2'] = "Corporate Security"
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"]=="BTS Corp Security") &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
            , 'customized RC1 Tier 3'] = "BTS Corp Security"


    # ----------------------------------- CPC Team Case A --------------------
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"] == "CPC team") &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
            , 'customized RC1 Tier 1'] = "Access & Vandalism"
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"] == "CPC team") &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "Account payable"
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"] == "CPC team") &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "CPC"
    # --------------------------------------- External Affairs Case A
    file.loc[
             # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
             # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
             # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
            (file["Support Group"] == "External Affairs") &
            ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Access & Vandalism"
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"] == "External Affairs") &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "Regulatory & governmental"
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"] == "External Affairs") &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "External Affairs"

    # -----------------------------------  Mobile Resources Acquisition Case A
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"] == "Mobile Resources Acquisition") &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Access & Vandalism"
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"] == "Mobile Resources Acquisition") &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "Mobile Resources Acquisition"
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"] == "Mobile Resources Acquisition") &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "Resources Acquisition"
    # ------------------------------------ Fixed Resources Acquisition Case A
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"] == "Fixed Resources Acquisition") &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Access & Vandalism"
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"] == "Fixed Resources Acquisition") &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "Fixed Resources Acquisition"
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"] == "Fixed Resources Acquisition") &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "Resources Acquisition"
    # ------------------------------  Health & Safety Management Case A
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"] == "Health & Safety Management") &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Access & Vandalism"
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
             (file["Support Group"] == "Health & Safety Management") &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "Fixed Resources Acquisition"
    file.loc[
              # ((file["Root Cause1 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause2 Tier 1"] != "Access & Vandalism") &
              # (file["Root Cause3 Tier 1"] != "Access & Vandalism")) &
              (file["Support Group"] == "Health & Safety Management") &
              ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "Resources Acquisition"
    # ------------------- other team support group with access and vandalism
    file.loc[
              ((file["Root Cause1 Tier 1"] == "Access & Vandalism") |
              (file["Root Cause2 Tier 1"] == "Access & Vandalism") |
              (file["Root Cause3 Tier 1"] == "Access & Vandalism")) &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Access & Vandalism"
    file.loc[
              ((file["Root Cause1 Tier 1"] == "Access & Vandalism") |
              (file["Root Cause2 Tier 1"] == "Access & Vandalism") |
              (file["Root Cause3 Tier 1"] == "Access & Vandalism")) &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "Other"
    file.loc[
              ((file["Root Cause1 Tier 1"] == "Access & Vandalism") |
              (file["Root Cause2 Tier 1"] == "Access & Vandalism") |
              (file["Root Cause3 Tier 1"] == "Access & Vandalism")) &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "Other"

    # ----------------------------- support group == MCC & Field activities -Network Service
    file.loc[(file["Support Group"] == "MCC & Field activities -Network Service") &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Planned Activity"
    file.loc[(file["Support Group"] == "MCC & Field activities -Network Service") &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "RO-PA"
    file.loc[(file["Support Group"] == "MCC & Field activities -Network Service") &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "Rollout and Upgrade"
    # ----------------------------- support group == Access Planned Activities
    file.loc[(file["Support Group"] == "Access Planned Activities") &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Planned Activity"
    file.loc[(file["Support Group"] == "Access Planned Activities") &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "SM-PA"
    file.loc[(file["Support Group"] == "Access Planned Activities") &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "SM-PA"
    # ------------- RC planned activity and Supported company Service management
    file.loc[((file["Root Cause1 Tier 1"] == "planned activity") |
              (file["Root Cause2 Tier 1"] == "planned activity") |
              (file["Root Cause3 Tier 1"] == "planned activity")) &
             (file["Support Company"] == "Service Management") &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Planned Activity"
    file.loc[((file["Root Cause1 Tier 1"] == "planned activity") |
              (file["Root Cause2 Tier 1"] == "planned activity") |
              (file["Root Cause3 Tier 1"] == "planned activity")) &
             (file["Support Company"] == "Service Management") &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "SM-PA"
    file.loc[((file["Root Cause1 Tier 1"] == "planned activity") |
              (file["Root Cause2 Tier 1"] == "planned activity") |
              (file["Root Cause3 Tier 1"] == "planned activity")) &
              (file["Support Company"] == "Service Management") &
              ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "SM-PA"
    # >>> searchfor = ['og', 'at']
    # >>> s[s.str.contains('|'.join(searchfor))]
    # ----------------------------- support group following teams or contains the following words
    teams_list=["Rollout Alex & North Coast","Rollout Cairo","Delta Rollout"
                ,"Rollout Giza","Rollout Upper-Red Sea&Sinai Region","RF & TX Implementation Cairo"
                "Network Services-RF-Implementation team","Giza implementation","TX Implementation",
                "Alex Region-TX&RF Upgrade","TX & RF upgrades team","Delta Telecom Acceptance",
                "Civil Acceptance & NTRA Delta & Alex & Upper","Civil Maintenance Team",
                # "Performance Audit Drive Test",
                "IBS Team",
                # "Legal Team",
                "Upper Telecom Acceptance",
                "Power & Environmental Acceptance",
                "Alex & Giza Telecom Acceptance","In-house Team"]
    contain_team_list=["Rollout","Implementation","upgrade"]
    file.loc[((file["Support Group"].isin(teams_list))|
              (file["Support Group"].str.contains("Implementation")|
               file["Support Group"].str.contains("Rollout")|
               file["Support Group"].str.contains("upgrade")))&
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Planned Activity"
    file.loc[((file["Support Group"].isin(teams_list))|
              (file["Support Group"].str.contains("Implementation")|
               file["Support Group"].str.contains("Rollout")|
               file["Support Group"].str.contains("upgrade"))) &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "RO-PA"
    file.loc[((file["Support Group"].isin(teams_list))|
              (file["Support Group"].str.contains("Implementation")|
               file["Support Group"].str.contains("Rollout")|
               file["Support Group"].str.contains("upgrade"))) &
              ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "Rollout and Upgrade "
    # ----------------------------- NFM and planned Acitivity
    file.loc[((file["Root Cause1 Tier 1"] == "planned activity") |
              (file["Root Cause2 Tier 1"] == "planned activity") |
              (file["Root Cause3 Tier 1"] == "planned activity")) &
             (file["Support Group"].str.contains("NFM")) &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Planned Activity"
    file.loc[((file["Root Cause1 Tier 1"] == "planned activity") |
              (file["Root Cause2 Tier 1"] == "planned activity") |
              (file["Root Cause3 Tier 1"] == "planned activity")) &
             (file["Support Group"].str.contains("NFM")) &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "RO-PA"
    file.loc[((file["Root Cause1 Tier 1"] == "planned activity") |
              (file["Root Cause2 Tier 1"] == "planned activity") |
              (file["Root Cause3 Tier 1"] == "planned activity")) &
             (file["Support Company"] != "Service Management") &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "L1 Maintenance"
    # ------------- RC planned activity and Supported company not Service management
    file.loc[((file["Root Cause1 Tier 1"] == "planned activity") |
              (file["Root Cause2 Tier 1"] == "planned activity") |
              (file["Root Cause3 Tier 1"] == "planned activity")) &
             (file["Support Company"] != "Service Management") &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Planned Activity"
    file.loc[((file["Root Cause1 Tier 1"] == "planned activity") |
              (file["Root Cause2 Tier 1"] == "planned activity") |
              (file["Root Cause3 Tier 1"] == "planned activity")) &
             (file["Support Company"] != "Service Management") &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "RO-PA"
    file.loc[((file["Root Cause1 Tier 1"] == "planned activity") |
              (file["Root Cause2 Tier 1"] == "planned activity") |
              (file["Root Cause3 Tier 1"] == "planned activity")) &
             (file["Support Group"].str.contains("NFM")) &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
             , 'customized RC1 Tier 3'] = "L1 Maintenance"
    # ------------------------ RC Power -------------------------
    # ------------------------- RC Power and Tier 3 “Stolen” or “Faulty” -------------
    # ------------------------------------  Tier 1
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Faulty")|
              file["Root Cause1 Tier 3"].str.contains("Stolen")) &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
             , 'customized RC1 Tier 1'] = "Power"
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Faulty")|
              file["Root Cause2 Tier 3"].str.contains("Stolen")) &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
             , 'customized RC1 Tier 1'] = "Power"
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Faulty")|
              file["Root Cause3 Tier 3"].str.contains("Stolen")) &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
             , 'customized RC1 Tier 1'] = "Power"

    # ------------------------------------  Tier 2
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Faulty")|
              file["Root Cause1 Tier 3"].str.contains("Stolen")) &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
             , 'customized RC1 Tier 2'] = "Backup Problem"

    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Faulty")|
              file["Root Cause2 Tier 3"].str.contains("Stolen")) &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
             , 'customized RC1 Tier 2'] = "Backup Problem"

    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Faulty")|
              file["Root Cause3 Tier 3"].str.contains("Stolen")) &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
             , 'customized RC1 Tier 2'] = "Backup Problem"

    # ------------------------------------  Tier 3
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Faulty")) &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
             , 'customized RC1 Tier 3'] = "Batteries Faulty"

    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Stolen")) &
             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "Batteries Stolen"

    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Faulty")) &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
             , 'customized RC1 Tier 3'] = "Batteries Faulty"
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Stolen")) &
             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
             , 'customized RC1 Tier 3'] = "Batteries Stolen"
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Faulty")) &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
             , 'customized RC1 Tier 3'] = "Batteries Faulty"
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Stolen")) &
             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
             , 'customized RC1 Tier 3'] = "Batteries Stolen"

    # ----------- Power Tier 1
    # ----------- using backup sheet
    # ------------------------------------  Tier 1
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Automated"))&
             (file["backup problem"]=="Yes" ) &
             ((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Power"
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Automated"))&
             (file["backup problem"]=="Yes" ) &
             ((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Power"
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Automated"))&
             (file["backup problem"]=="Yes" ) &
             ((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Power"

    # ------------------------------------  Tier 2
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Automated"))&
             (file["backup problem"]=="Yes" ) &
             ((file['customized RC1 Tier 2'] == "N/A") | (file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "Backup Problem"

    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Automated"))&
             (file["backup problem"]=="Yes" ) &
             ((file['customized RC1 Tier 2'] == "N/A") | (file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "Backup Problem"

    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Automated"))&
             (file["backup problem"]=="Yes" ) &
             ((file['customized RC1 Tier 2'] == "N/A") | (file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "Backup Problem"

    # ------------------------------------  Tier 3
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Automated"))&
             (file["backup problem"]=="Yes" ) &
             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "Backup Issue"


    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Automated"))&
             (file["backup problem"]=="Yes" ) &
             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "Backup Issue"

    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Automated"))&
             (file["backup problem"]=="Yes" ) &
             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "Backup Issue"

    #    power
    # ----------- using power sheet
    # ------------------------------------  Tier 1
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Automated"))&

             ((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Power"
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Automated"))&

             ((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Power"
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Automated"))&

             ((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Power"

    # ------------------------------------  Tier 2
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Automated"))&

             ((file['customized RC1 Tier 2'] == "N/A") | (file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Automated"))&
             ((file['customized RC1 Tier 2'] == "N/A") | (file["customized RC1 Tier 2"].isnull()))
    , 'Site Power Source']

    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Automated"))&

             ((file['customized RC1 Tier 2'] == "N/A") | (file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Automated"))&
             ((file['customized RC1 Tier 2'] == "N/A") | (file["customized RC1 Tier 2"].isnull()))
    , 'Site Power Source']

    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Automated"))&

             ((file['customized RC1 Tier 2'] == "N/A") | (file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Automated"))&

             ((file['customized RC1 Tier 2'] == "N/A") | (file["customized RC1 Tier 2"].isnull()))
    , 'Site Power Source']

    # ------------------------------------  Tier 3
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Automated"))&

             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Automated"))&

             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause1 Tier 3']



    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Automated"))&

             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Automated"))&

             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause2 Tier 3']

    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Automated"))&

             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Automated"))&

             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause3 Tier 3']

    # ------------------------ power sharing

    # ------------------------------------  Tier 1
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Mobinil")|
              file["Root Cause1 Tier 3"].str.contains("Etisalat")) &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
             , 'customized RC1 Tier 1'] = "Sharing"
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Mobinil")|
              file["Root Cause2 Tier 3"].str.contains("Etisalat")) &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
             , 'customized RC1 Tier 1'] = "Sharing"
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Mobinil")|
              file["Root Cause3 Tier 3"].str.contains("Etisalat")) &
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
             , 'customized RC1 Tier 1'] = "Sharing"

    # ------------------------------------  Tier 2
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Mobinil")|
              file["Root Cause1 Tier 3"].str.contains("Etisalat")) &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
             , 'customized RC1 Tier 2'] = "Sharing Problem"

    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Mobinil")|
              file["Root Cause2 Tier 3"].str.contains("Etisalat")) &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
             , 'customized RC1 Tier 2'] = "Sharing Problem"

    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Mobinil")|
              file["Root Cause3 Tier 3"].str.contains("Etisalat")) &
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
             , 'customized RC1 Tier 2'] = "Sharing Problem"

    # ------------------------------------  Tier 3
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Mobinil")) &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
             , 'customized RC1 Tier 3'] = "Orange Generator"

    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 3"].str.contains("Etisalat")) &
             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "Etisalat Generator"

    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Mobinil")) &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
             , 'customized RC1 Tier 3'] = "Orange Generator"
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 3"].str.contains("Etisalat")) &
             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
             , 'customized RC1 Tier 3'] = "Etisalat Generator"
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Mobinil")) &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
             , 'customized RC1 Tier 3'] = "Orange Generator"
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 3"].str.contains("Etisalat")) &
             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
             , 'customized RC1 Tier 3'] = "Etisalat Generator"

    # ------------------------- RC Power and Tier 2 “Generator” -------------
    # ------------------------------------  Tier 1
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 2"].str.contains("Generator") )&
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause1 Tier 2"].str.contains("Generator") )&
                                          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'Root Cause1 Tier 1']
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 2"].str.contains("Generator") )&
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause2 Tier 2"].str.contains("Generator") )&
                                          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'Root Cause2 Tier 1']
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 2"].str.contains("Generator") )&
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause3 Tier 1"] == "Power") &
                                          (file["Root Cause3 Tier 2"].str.contains("Generator") )&
                                          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'Root Cause3 Tier 1']

    # ------------------------------------  Tier 2
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 2"].str.contains("Generator") )&
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause1 Tier 2"].str.contains("Generator") )&
                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'Root Cause1 Tier 2']
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 2"].str.contains("Generator") )&
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause2 Tier 2"].str.contains("Generator") )&
                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'Root Cause2 Tier 2']
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 2"].str.contains("Generator") )&
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause3 Tier 1"] == "Power") &
                                          (file["Root Cause3 Tier 2"].str.contains("Generator") )&
                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'Root Cause3 Tier 2']

    # ------------------------------------  Tier 3
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 2"].str.contains("Generator") )&
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause1 Tier 2"].str.contains("Generator") )&
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause1 Tier 3']
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 2"].str.contains("Generator") )&
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause2 Tier 2"].str.contains("Generator") )&
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause2 Tier 3']
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 2"].str.contains("Generator") )&
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause3 Tier 1"] == "Power") &
                                          (file["Root Cause3 Tier 2"].str.contains("Generator") )&
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause3 Tier 3']


    # ------------------------- RC Power and Tier 2 “Power Cube” -------------
    # ------------------------------------  Tier 1
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 2"].str.contains("Power Cube") )&
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause1 Tier 2"].str.contains("Power Cube") )&
                                          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'Root Cause1 Tier 1']
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 2"].str.contains("Power Cube") )&
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause2 Tier 2"].str.contains("Power Cube") )&
                                          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'Root Cause2 Tier 1']
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 2"].str.contains("Power Cube") )&
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause3 Tier 1"] == "Power") &
                                          (file["Root Cause3 Tier 2"].str.contains("Power Cube") )&
                                          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'Root Cause3 Tier 1']

    # ------------------------------------  Tier 2
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 2"].str.contains("Power Cube") )&
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause1 Tier 2"].str.contains("Power Cube") )&
                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'Root Cause1 Tier 2']
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 2"].str.contains("Power Cube") )&
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause2 Tier 2"].str.contains("Power Cube") )&
                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'Root Cause2 Tier 2']
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 2"].str.contains("Power Cube") )&
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause3 Tier 1"] == "Power") &
                                          (file["Root Cause3 Tier 2"].str.contains("Power Cube") )&
                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'Root Cause3 Tier 2']

    # ------------------------------------  Tier 3
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 2"].str.contains("Power Cube") )&
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause1 Tier 2"].str.contains("Power Cube") )&
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause1 Tier 3']
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 2"].str.contains("Power Cube") )&
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause2 Tier 2"].str.contains("Power Cube") )&
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause2 Tier 3']
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 2"].str.contains("Power Cube") )&
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause3 Tier 1"] == "Power") &
                                          (file["Root Cause3 Tier 2"].str.contains("Power Cube") )&
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause3 Tier 3']


    # ------------------------- RC Power and Tier 2 “Power-AC” -------------
    # ------------------------------------  Tier 1
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 2"].str.contains("Power-AC") )&
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
             , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause1 Tier 2"].str.contains("Power-AC") )&
                                          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
                                          , 'Root Cause1 Tier 1']
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 2"].str.contains("Power-AC") )&
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause2 Tier 2"].str.contains("Power-AC") )&
                                          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'Root Cause2 Tier 1']
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 2"].str.contains("Power-AC") )&
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause3 Tier 1"] == "Power") &
                                          (file["Root Cause3 Tier 2"].str.contains("Power-AC") )&
                                          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'Root Cause3 Tier 1']

    # ------------------------------------  Tier 2
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 2"].str.contains("Power-AC") )&
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause1 Tier 2"].str.contains("Power-AC") )&
                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'Root Cause1 Tier 2']
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 2"].str.contains("Power-AC") )&
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause2 Tier 2"].str.contains("Power-AC") )&
                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'Root Cause2 Tier 2']
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 2"].str.contains("Power-AC") )&
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause3 Tier 1"] == "Power") &
                                          (file["Root Cause3 Tier 2"].str.contains("Power-AC") )&
                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'Root Cause3 Tier 2']

    # ------------------------------------  Tier 3
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &
             (file["Root Cause1 Tier 2"].str.contains("Power-AC") )&
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause1 Tier 2"].str.contains("Power-AC") )&
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause1 Tier 3']
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &
             (file["Root Cause2 Tier 2"].str.contains("Power-AC") )&
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &
                                          (file["Root Cause2 Tier 2"].str.contains("Power-AC") )&
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause2 Tier 3']
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &
             (file["Root Cause3 Tier 2"].str.contains("Power-AC") )&
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause3 Tier 1"] == "Power") &
                                          (file["Root Cause3 Tier 2"].str.contains("Power-AC") )&
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause3 Tier 3']
    # ------------------------- RC Tier1 Power  -------------
    # ------------------------------------  Tier 1
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &

             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &

                                          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'Root Cause1 Tier 1']
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &

             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &

                                          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'Root Cause2 Tier 1']
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &

             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause3 Tier 1"] == "Power") &

                                          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'Root Cause3 Tier 1']

    # ------------------------------------  Tier 2
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &

             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &

                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'Root Cause1 Tier 2']
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &

             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &

                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'Root Cause2 Tier 2']
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &

             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause3 Tier 1"] == "Power") &

                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'Root Cause3 Tier 2']

    # ------------------------------------  Tier 3
    # ----------RC1
    file.loc[(file["Root Cause1 Tier 1"] == "Power") &

             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &

                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause1 Tier 3']
    # ----------- RC2
    file.loc[(file["Root Cause2 Tier 1"] == "Power") &

             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 1"] == "Power") &

                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause2 Tier 3']
    # ------------ RC3
    file.loc[(file["Root Cause3 Tier 1"] == "Power") &

             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause3 Tier 1"] == "Power") &

                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause3 Tier 3']
    # ------------------------------ if only RC1 is exist
    file.loc[
             (file["Root Cause2 Tier 3"].isnull()) &
             (file["Root Cause3 Tier 3"].isnull())&
             ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[
                                          (file["Root Cause2 Tier 3"].isnull()) &
                                          (file["Root Cause3 Tier 3"].isnull())&
                                          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
                                          , "Root Cause1 Tier 1"]

    file.loc[
             (file["Root Cause2 Tier 3"].isnull()) &
             (file["Root Cause3 Tier 3"].isnull())&
             ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
             , 'customized RC1 Tier 2'] = file.loc[
                                          (file["Root Cause2 Tier 3"].isnull()) &
                                          (file["Root Cause3 Tier 3"].isnull())&

                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
                                          , "Root Cause1 Tier 2"]
    file.loc[
             (file["Root Cause2 Tier 3"].isnull()) &
             (file["Root Cause3 Tier 3"].isnull())&

             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[
                                          (file["Root Cause2 Tier 3"].isnull()) &
                                          (file["Root Cause3 Tier 3"].isnull())&
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
                                        , "Root Cause1 Tier 3"]
    # ------------------------------------------------------------------------------------------------
    # "Categorization Tier 1"
    free_rc_mapping_Tier1 = {
        "Field Tx node": "TX Access", "VF Core TX problem": "TX Backhaul", "Environmental": "Environmental",
        "Power": "Power", "Telecom": "Telecom Problem", "TE Core Tx problem": "TX Backhaul",
        "Microwave": "TX Access", "Generator": "Power", "VF Core Tx Problem": "TX Backhaul",
        "Performance Problem": "Telecom Problem", "Radio": "Telecom Problem", "Solar Power": "Power",
    }
    free_rc_mapping_Tier2 = {
        "Field Tx node": "TX Access Automated Resolution", "VF Core TX problem": "TX Backhaul Automated Resolution",
        "Environmental": "Environmental Automated Resolution", "Power": "Power Automated Resolution",
        "Telecom": "Telecom Problem Automated Resolution", "TE Core Tx problem": "TX Backhaul Automated Resolution",
        "Microwave": "TX Access Automated Resolution", "VF Core Tx Problem": "TX Backhaul Automated Resolution",
        "Generator": "Generator Automated Resolution",
        "Performance Problem": "Performance Problem Automated Resolution",
        "Radio": "Telecom Problem Automated Resolution", "Solar Power": "Solar Power Automated Resolution",
    }
    free_rc_mapping_Tier3 = {
        "Field Tx node": "TX Access Automated Resolution", "VF Core TX problem": "TX Backhaul Automated Resolution",
        "Environmental": "Environmental Automatic Resolution", "Power": "Power Automated Resolution",
        "Telecom": "Telecom Problem Automated Resolution", "TE Core Tx problem": "Transmission TE Automated Resolution",
        "Microwave": "TX Access Automated Resolution", "VF Core Tx Problem": "TX Fluctuation Automatic Resolution",
        "Generator": "Generator Automated Resolution",
        "Performance Problem": "Performance Problem Automated Resolution",
        "Radio": "Telecom Problem Automated Resolution", "Solar Power": "Solar Power Automated Resolution",

    }
    file.loc[(file["Root Cause1 Tier 3"].isnull()) &
             (file["Root Cause2 Tier 3"].isnull()) &
             (file["Root Cause3 Tier 3"].isnull())&
             (((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))|(file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause1 Tier 3"].isnull()) &
                                          (file["Root Cause2 Tier 3"].isnull()) &
                                          (file["Root Cause3 Tier 3"].isnull())&
                                          ((file['customized RC1 Tier 1'] == "N/A")|(file["customized RC1 Tier 1"].isnull()))
    , "Categorization Tier 1"].map(free_rc_mapping_Tier1, na_action='ignore')

    file.loc[(file["Root Cause1 Tier 3"].isnull()) &
             (file["Root Cause2 Tier 3"].isnull()) &
             (file["Root Cause3 Tier 3"].isnull())&
                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 3"].isnull()) &
                                          (file["Root Cause2 Tier 3"].isnull()) &
                                          (file["Root Cause3 Tier 3"].isnull())&
                                          ((file['customized RC1 Tier 2'] == "N/A")|(file["customized RC1 Tier 2"].isnull()))
    , "Categorization Tier 1"].map(free_rc_mapping_Tier2, na_action='ignore')
    file.loc[(file["Root Cause1 Tier 3"].isnull()) &
             (file["Root Cause2 Tier 3"].isnull()) &
             (file["Root Cause3 Tier 3"].isnull())&
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 3"].isnull()) &
                                          (file["Root Cause2 Tier 3"].isnull()) &
                                          (file["Root Cause3 Tier 3"].isnull())&
                                          ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
    , "Categorization Tier 1"].map(free_rc_mapping_Tier3, na_action='ignore')

    # ------------------------------------------------------ preparation for RC
    # ------------------   RC1 Tier 3 = RC2 Tier 3 = RC3 Tier 3
    # -------------Tier 1
    file.loc[(file["Root Cause1 Tier 3"]== (file["Root Cause2 Tier 3"]))&
             (file["Root Cause2 Tier 3"]==(file["Root Cause3 Tier 3"])) &
             ((file['customized RC1 Tier 3'] == "N/A")|
              (file["customized RC1 Tier 3"].isnull()))
            , 'customized RC1 Tier 1']= file.loc[(file["Root Cause1 Tier 3"]== (file["Root Cause2 Tier 3"]))&
             (file["Root Cause2 Tier 3"]==(file["Root Cause3 Tier 3"])) &
             ((file['customized RC1 Tier 3'] == "N/A")|(file["customized RC1 Tier 3"].isnull()))
             , 'Root Cause1 Tier 1']

    # -------------Tier 2
    file.loc[(file["Root Cause1 Tier 3"] == (file["Root Cause2 Tier 3"])) &
              (file["Root Cause2 Tier 3"] == (file["Root Cause3 Tier 3"])) &
              ((file['customized RC1 Tier 3'] == "N/A") |
               (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 3"] == (file["Root Cause2 Tier 3"])) &
                                           (file["Root Cause2 Tier 3"] == (file["Root Cause3 Tier 3"])) &
                                           ((file['customized RC1 Tier 3'] == "N/A") |
                                            (file["customized RC1 Tier 3"].isnull())), 'Root Cause1 Tier 2']


    # -------- Tier 3

    file.loc[(file["Root Cause1 Tier 3"] == (file["Root Cause2 Tier 3"])) &
              (file["Root Cause2 Tier 3"] == (file["Root Cause3 Tier 3"])) &
              ((file['customized RC1 Tier 3'] == "N/A") |
               (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 3"] == (file["Root Cause2 Tier 3"])) &
                                           (file["Root Cause2 Tier 3"] == (file["Root Cause3 Tier 3"])) &
                                           ((file['customized RC1 Tier 3'] == "N/A") |
                                            (file["customized RC1 Tier 3"].isnull())), 'Root Cause1 Tier 3']


    # ------------------   RC1 Tier 3 = RC2 Tier 3 and  RC3 Tier 3 is null
    # -------------Tier 1
    file.loc[(file["Root Cause1 Tier 3"]== (file["Root Cause2 Tier 3"]))&
             ((file["Root Cause3 Tier 3"].isnull())) &
             ((file['customized RC1 Tier 3'] == "N/A")|
              (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 1']= file.loc[(file["Root Cause1 Tier 3"]== (file["Root Cause2 Tier 3"]))&
             ((file["Root Cause3 Tier 3"].isnull())) &
             ((file['customized RC1 Tier 3'] == "N/A")|
              (file["customized RC1 Tier 3"].isnull())), 'Root Cause1 Tier 1']

    # -------------Tier 2
    file.loc[(file["Root Cause1 Tier 3"] == (file["Root Cause2 Tier 3"])) &
              ((file["Root Cause3 Tier 3"].isnull())) &
              ((file['customized RC1 Tier 3'] == "N/A") |
               (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 3"] == (file["Root Cause2 Tier 3"])) &
                                           ((file["Root Cause3 Tier 3"].isnull())) &
                                           ((file['customized RC1 Tier 3'] == "N/A") |
                                            (file["customized RC1 Tier 3"].isnull())), 'Root Cause1 Tier 2']


    # -------- Tier 3

    file.loc[(file["Root Cause1 Tier 3"] == (file["Root Cause2 Tier 3"])) &
              ((file["Root Cause3 Tier 3"].isnull())) &
              ((file['customized RC1 Tier 3'] == "N/A") |
               (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 3"] == (file["Root Cause2 Tier 3"])) &
                                           ((file["Root Cause3 Tier 3"].isnull())) &
                                           ((file['customized RC1 Tier 3'] == "N/A") |
                                            (file["customized RC1 Tier 3"].isnull())), 'Root Cause1 Tier 3']

    # ------------------ RC1 and RC2 and RC3 Tier3 have autolist or RC3 is empty result multiple
    autolist=["Up with no action","Clear After Reset","Restart due to Suspected Hang","SW Problem","Up With no Action"]
    file.loc[(file["Root Cause1 Tier 3"].isin(autolist)|file["Root Cause1 Tier 3"].str.contains("Auto")) &
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &
             (file["Root Cause3 Tier 3"].isin(autolist)|file["Root Cause3 Tier 3"].str.contains("Auto")|file["Root Cause3 Tier 3"].isnull()) &
             (((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull())) | (
                 file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = "Multiple"


    file.loc[(file["Root Cause1 Tier 3"].isin(autolist)|file["Root Cause1 Tier 3"].str.contains("Auto")) &
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &
             (file["Root Cause3 Tier 3"].isin(autolist)|file["Root Cause3 Tier 3"].str.contains("Auto")|file["Root Cause3 Tier 3"].isnull()) &
             ((file['customized RC1 Tier 2'] == "N/A") | (file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = "Multiple"

    file.loc[(file["Root Cause1 Tier 3"].isin(autolist)|file["Root Cause1 Tier 3"].str.contains("Auto")) &
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &
             (file["Root Cause3 Tier 3"].isin(autolist)|file["Root Cause3 Tier 3"].str.contains("Auto")|file["Root Cause3 Tier 3"].isnull()) &
             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = "Multiple"


    # ------------------ RC2 auto and RC3 auto or RC3 empty result will be RC1

    file.loc[
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &
             (file["Root Cause3 Tier 3"].isin(autolist)|file["Root Cause3 Tier 3"].str.contains("Auto")|file["Root Cause3 Tier 3"].isnull()) &
             (((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull())) | (
                 file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &
             (file["Root Cause3 Tier 3"].isin(autolist)|file["Root Cause3 Tier 3"].str.contains("Auto")|file["Root Cause3 Tier 3"].isnull()) &
             (((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull())) | (
                 file["customized RC1 Tier 1"].isnull()))
    , 'Root Cause1 Tier 1']


    file.loc[
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &
             (file["Root Cause3 Tier 3"].isin(autolist)|file["Root Cause3 Tier 3"].str.contains("Auto")|file["Root Cause3 Tier 3"].isnull()) &
             ((file['customized RC1 Tier 2'] == "N/A") | (file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &
             (file["Root Cause3 Tier 3"].isin(autolist)|file["Root Cause3 Tier 3"].str.contains("Auto")|file["Root Cause3 Tier 3"].isnull()) &
             (((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull())) | (
                 file["customized RC1 Tier 1"].isnull()))
    , 'Root Cause1 Tier 2']

    file.loc[
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &
             (file["Root Cause3 Tier 3"].isin(autolist)|file["Root Cause3 Tier 3"].str.contains("Auto")|file["Root Cause3 Tier 3"].isnull()) &
             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &
             (file["Root Cause3 Tier 3"].isin(autolist)|file["Root Cause3 Tier 3"].str.contains("Auto")|file["Root Cause3 Tier 3"].isnull()) &
             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause1 Tier 3']

    # ------------------ RC1 auto and RC3 auto or RC3 empty result will be RC2

    file.loc[
        (file["Root Cause1 Tier 3"].isin(autolist) | file["Root Cause1 Tier 3"].str.contains("Auto")) &
        (file["Root Cause3 Tier 3"].isin(autolist) | file["Root Cause3 Tier 3"].str.contains("Auto") | file[
            "Root Cause3 Tier 3"].isnull()) &
        (((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull())) | (
            file["customized RC1 Tier 1"].isnull()))
        , 'customized RC1 Tier 1'] = file.loc[
        (file["Root Cause1 Tier 3"].isin(autolist) | file["Root Cause1 Tier 3"].str.contains("Auto")) &
        (file["Root Cause3 Tier 3"].isin(autolist) | file["Root Cause3 Tier 3"].str.contains("Auto") | file[
            "Root Cause3 Tier 3"].isnull()) &
        (((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull())) | (
            file["customized RC1 Tier 1"].isnull()))
        , 'Root Cause2 Tier 1']

    file.loc[
        (file["Root Cause1 Tier 3"].isin(autolist) | file["Root Cause1 Tier 3"].str.contains("Auto")) &
        (file["Root Cause3 Tier 3"].isin(autolist) | file["Root Cause3 Tier 3"].str.contains("Auto") | file[
            "Root Cause3 Tier 3"].isnull()) &
        ((file['customized RC1 Tier 2'] == "N/A") | (file["customized RC1 Tier 2"].isnull()))
        , 'customized RC1 Tier 2'] = file.loc[
        (file["Root Cause1 Tier 3"].isin(autolist) | file["Root Cause1 Tier 3"].str.contains("Auto")) &
        (file["Root Cause3 Tier 3"].isin(autolist) | file["Root Cause3 Tier 3"].str.contains("Auto") | file[
            "Root Cause3 Tier 3"].isnull()) &
        (((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull())) | (
            file["customized RC1 Tier 1"].isnull()))
        , 'Root Cause2 Tier 2']

    file.loc[
        (file["Root Cause1 Tier 3"].isin(autolist) | file["Root Cause1 Tier 3"].str.contains("Auto")) &
        (file["Root Cause3 Tier 3"].isin(autolist) | file["Root Cause3 Tier 3"].str.contains("Auto") | file[
            "Root Cause3 Tier 3"].isnull()) &
        ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
        , 'customized RC1 Tier 3'] = file.loc[
        (file["Root Cause1 Tier 3"].isin(autolist) | file["Root Cause1 Tier 3"].str.contains("Auto")) &
        (file["Root Cause3 Tier 3"].isin(autolist) | file["Root Cause3 Tier 3"].str.contains("Auto") | file[
            "Root Cause3 Tier 3"].isnull()) &
        ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
        , 'Root Cause2 Tier 3']



    # ------------------ RC1 and RC2 and RC3 Tier3 have autolist or RC3 is empty result multiple

    file.loc[(file["Root Cause1 Tier 3"].isin(autolist)|file["Root Cause1 Tier 3"].str.contains("Auto")) &
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &

             (((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull())) | (
                 file["customized RC1 Tier 1"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause1 Tier 3"].isin(autolist)|file["Root Cause1 Tier 3"].str.contains("Auto")) &
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &

             (((file['customized RC1 Tier 1'] == "N/A") | (file["customized RC1 Tier 1"].isnull())) | (
                 file["customized RC1 Tier 1"].isnull()))
    , 'Root Cause3 Tier 1']


    file.loc[(file["Root Cause1 Tier 3"].isin(autolist)|file["Root Cause1 Tier 3"].str.contains("Auto")) &
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &

             ((file['customized RC1 Tier 2'] == "N/A") | (file["customized RC1 Tier 2"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 3"].isin(autolist)|file["Root Cause1 Tier 3"].str.contains("Auto")) &
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &

             ((file['customized RC1 Tier 2'] == "N/A") | (file["customized RC1 Tier 2"].isnull()))
    , 'Root Cause3 Tier 2']

    file.loc[(file["Root Cause1 Tier 3"].isin(autolist)|file["Root Cause1 Tier 3"].str.contains("Auto")) &
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &

             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 3"].isin(autolist)|file["Root Cause1 Tier 3"].str.contains("Auto")) &
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &

             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause3 Tier 3']

    # ------------------   RC1 Tier 3 = RC2 Tier 3  and RC3 Tier 3 auto or RC2 Tier 3 = RC3 Tier 3 and RC1 Tier 3 auto
    # -------------Tier 1
    file.loc[(((file["Root Cause1 Tier 3"] == (file["Root Cause2 Tier 3"]))&((file["Root Cause3 Tier 3"].isin(autolist)|file["Root Cause3 Tier 3"].str.contains("Auto")))) |
             (file["Root Cause2 Tier 3"] == (file["Root Cause3 Tier 3"]))&((file["Root Cause1 Tier 3"].isin(autolist)|file["Root Cause1 Tier 3"].str.contains("Auto")))) &
             ((file['customized RC1 Tier 3'] == "N/A") |(file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(((file["Root Cause1 Tier 3"] == (file["Root Cause2 Tier 3"]))&((file["Root Cause3 Tier 3"].isin(autolist)|file["Root Cause3 Tier 3"].str.contains("Auto")))) |
             (file["Root Cause2 Tier 3"] == (file["Root Cause3 Tier 3"]))&((file["Root Cause1 Tier 3"].isin(autolist)|file["Root Cause1 Tier 3"].str.contains("Auto")))) &
             ((file['customized RC1 Tier 3'] == "N/A") |(file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause2 Tier 1']

    # -------------Tier 2
    file.loc[(((file["Root Cause1 Tier 3"] == (file["Root Cause2 Tier 3"])) & (
    (file["Root Cause3 Tier 3"].isin(autolist) | file["Root Cause3 Tier 3"].str.contains("Auto")))) |
              (file["Root Cause2 Tier 3"] == (file["Root Cause3 Tier 3"])) & (
              (file["Root Cause1 Tier 3"].isin(autolist) | file["Root Cause1 Tier 3"].str.contains("Auto")))) &
             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(((file["Root Cause1 Tier 3"] == (file["Root Cause2 Tier 3"]))&((file["Root Cause3 Tier 3"].isin(autolist)|file["Root Cause3 Tier 3"].str.contains("Auto")))) |
             (file["Root Cause2 Tier 3"] == (file["Root Cause3 Tier 3"]))&((file["Root Cause1 Tier 3"].isin(autolist)|file["Root Cause1 Tier 3"].str.contains("Auto")))) &
             ((file['customized RC1 Tier 3'] == "N/A") |(file["customized RC1 Tier 3"].isnull())), 'Root Cause2 Tier 2']

    # -------- Tier 3

    file.loc[(((file["Root Cause1 Tier 3"] == (file["Root Cause2 Tier 3"])) & (
    (file["Root Cause3 Tier 3"].isin(autolist) | file["Root Cause3 Tier 3"].str.contains("Auto")))) |
              (file["Root Cause2 Tier 3"] == (file["Root Cause3 Tier 3"])) & (
              (file["Root Cause1 Tier 3"].isin(autolist) | file["Root Cause1 Tier 3"].str.contains("Auto")))) &
             ((file['customized RC1 Tier 3'] == "N/A") | (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(((file["Root Cause1 Tier 3"] == (file["Root Cause2 Tier 3"]))&((file["Root Cause3 Tier 3"].isin(autolist)|file["Root Cause3 Tier 3"].str.contains("Auto")))) |
             (file["Root Cause2 Tier 3"] == (file["Root Cause3 Tier 3"]))&((file["Root Cause1 Tier 3"].isin(autolist)|file["Root Cause1 Tier 3"].str.contains("Auto")))) &
             ((file['customized RC1 Tier 3'] == "N/A") |(file["customized RC1 Tier 3"].isnull())), 'Root Cause2 Tier 3']

    # ------------------   RC1 Tier 3  = RC3 Tier 3 and RC2 Tier 3 auto
    # -------------Tier 1
    file.loc[(file["Root Cause1 Tier 3"] == (file["Root Cause3 Tier 3"])) &
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &
             ((file['customized RC1 Tier 3'] == "N/A") |
              (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 1'] = file.loc[(file["Root Cause1 Tier 3"] == (file["Root Cause3 Tier 3"])) &
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &
             ((file['customized RC1 Tier 3'] == "N/A") |
              (file["customized RC1 Tier 3"].isnull()))
    , 'Root Cause1 Tier 1']

    # -------------Tier 2
    file.loc[(file["Root Cause1 Tier 3"] == (file["Root Cause3 Tier 3"])) &
             (file["Root Cause2 Tier 3"].isin(autolist) | file["Root Cause2 Tier 3"].str.contains("Auto")) &
             ((file['customized RC1 Tier 3'] == "N/A") |
              (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 2'] = file.loc[(file["Root Cause1 Tier 3"] == (file["Root Cause3 Tier 3"])) &
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &
             ((file['customized RC1 Tier 3'] == "N/A") |
              (file["customized RC1 Tier 3"].isnull())), 'Root Cause1 Tier 2']

    # -------- Tier 3

    file.loc[(file["Root Cause1 Tier 3"] == (file["Root Cause3 Tier 3"])) &
             (file["Root Cause2 Tier 3"].isin(autolist) | file["Root Cause2 Tier 3"].str.contains("Auto")) &
             ((file['customized RC1 Tier 3'] == "N/A") |
              (file["customized RC1 Tier 3"].isnull()))
    , 'customized RC1 Tier 3'] = file.loc[(file["Root Cause1 Tier 3"] == (file["Root Cause3 Tier 3"])) &
             (file["Root Cause2 Tier 3"].isin(autolist)|file["Root Cause2 Tier 3"].str.contains("Auto")) &
             ((file['customized RC1 Tier 3'] == "N/A") |
              (file["customized RC1 Tier 3"].isnull())), 'Root Cause1 Tier 3']


    return file



#
# start=time.time()
# df= pd.read_excel("Vodafone Losses Analysis Update July 2020 Version_ORG.xlsx")
#
# add_physical_technology(df,"Asset Id")
# df["Phy Site"] = df["Phy Site"].apply(pd.to_numeric, errors='coerce').fillna(df["Phy Site"])
# df=add_site_unified_power_source(df)
# df=add_guard(df)
# df=add_north_sinai(df)
# df=add_backup_problem_ods(df)
# df["customized RC1 Tier 1"]="N/A"
# df["customized RC1 Tier 2"]="N/A"
# df["customized RC1 Tier 3"]="N/A"
# df=cust_RC(df)
# SM_df = pd.DataFrame()
# df.to_excel("NFM_RCA_Result.xlsx")
# SM_df=df[['Ref No','Incident Number','Asset Id','Total Loss','Phy Site','Technology','Radio Region','North Sinai','customized RC1 Tier 1','customized RC1 Tier 2','customized RC1 Tier 3']]
# SM_df.to_excel("SM_RCA_Result.xlsx")
#
# end=time.time()
#
# print(start-end)