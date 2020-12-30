from django.db import models
import datetime

# Create your models here.
class Contractor_DB(models.Model):

    
    Contractor_Name = models.CharField(max_length=30,blank=True)

    Existing = models.BooleanField(default=False)
    Civil = models.BooleanField(default=False)
    Civil_Active = models.BooleanField(default=False)
    Telecom = models.BooleanField(default=False)
    Telecom_Active = models.BooleanField(default=False)
    Civil_Enhancement = models.BooleanField(default=False)
    Civil_Enhancement_Active = models.BooleanField(default=False)
    # define functions
    def __str__(self):
        return self.Contractor_Name

class rollout_pool(models.Model):
    site_id =models.CharField(max_length=30,blank=True)

    # define Region list
    Alex = "Alex"
    Cairo = "Cairo"
    Delta = "Delta"
    Giza = "Giza"
    Upper = "Upper"

    region_choice = [(Alex,"Alex"),(Cairo,"Cairo"),(Delta,"Delta"),(Giza,"Giza"),(Upper,"Upper")]



    region = models.CharField(max_length=30,choices=region_choice,blank=False, null=True)

    Contractor = models.OneToOneField(Contractor_DB,on_delete=models.CASCADE)

    Pool = models.IntegerField( default=0)
    
    Date = models.DateField( auto_now=False, auto_now_add=False)

    
    Version = models.CharField(max_length=30,blank=True)

    FY=models.CharField(max_length=30,blank=True)
    def __str__(self):
        return self.site_id
    

class rollout_db(models.Model):
    Contractor = models.OneToOneField(Contractor_DB,on_delete=models.CASCADE)
    current_year=datetime.date.today().year
    FY = models.IntegerField( default=current_year)
    # define Region list
    Alex = "Alex"
    Cairo = "Cairo"
    Delta = "Delta"
    Giza = "Giza"
    Upper = "Upper"

    region_choice = [(Alex,"Alex"),(Cairo,"Cairo"),(Delta,"Delta"),(Giza,"Giza"),(Upper,"Upper")]



    region = models.CharField(max_length=30,choices=region_choice,blank=False, null=True)

    Allocation_from_Pool= models.IntegerField(default=0)
    NoOption=models.IntegerField(default=0)
    SF2=models.IntegerField(default=0)
    ApprovedSF3=models.IntegerField(default=0)
    SF51=models.IntegerField(default=0)
    Contract_Signed=models.IntegerField(default=0)
    RFC=models.IntegerField(default=0)
    RFI_SA=models.IntegerField(default=0)
    RFI_Sharing=models.IntegerField(default=0)
    RFI_Redeployment_Replacement=models.IntegerField(default=0)
    RFI_Total=models.IntegerField(default=0)
    Comment= models.CharField(max_length=200,blank=True)
    
    def __str__(self):
        return self.Contractor
    
class telecom_civil_db(models.Model):
    Contractor = models.ForeignKey(Contractor_DB,on_delete=models.CASCADE)
    # define Region list
    Alex = "Alex"
    Cairo = "Cairo"
    Delta = "Delta"
    Giza = "Giza"
    Upper = "Upper"

    region_choice = [(Alex,"Alex"),(Cairo,"Cairo"),(Delta,"Delta"),(Giza,"Giza"),(Upper,"Upper")]



    region = models.CharField(max_length=30,choices=region_choice,blank=False, null=True)

    Quarter = models.CharField(max_length=10,blank=True)
    Current_FY=models.CharField(max_length=10,blank=True)
    CivilupgradesTarget=models.IntegerField(default=0)
    CivilupgradesAchieved=models.IntegerField(default=0)
    Civilupgrades_Comment= models.CharField(max_length=200,blank=True)
    TelecomServicesTarget=models.IntegerField(default=0)
    TelecomservicesAchieved=models.IntegerField(default=0)
    Telecomservices_Comment= models.CharField(max_length=200,blank=True)
    Civilenhancementactivities_Target=models.IntegerField(default=0)
    Civilenhancementactivities_Achieved=models.IntegerField(default=0)
    Civilenhancementactivities_comment= models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.Contractor.Contractor_Name

class Ranking_db(models.Model):
    Contractor = models.OneToOneField(Contractor_DB,on_delete=models.CASCADE)
    Quarter =models.CharField(max_length=5,blank=True)
    Rollout_Total_assigned_Pool= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Sum_of_Rollout_RFI= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Percentage_to_Pool= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Percentage_to_First_RFI= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Rollout_20= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Rollout_80= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Rollout_score= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Rollout_Rank= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Civil_Upgrades_total_Target= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Civil_Upgrades_total_Achieved= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Civil_Ach_to_Target= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Civil_Ach_to_First= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Weight_of_Civil_Target= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Weight_of_Civil_Ach= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Civil_Upgrades_Score= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Civil_Upgrades_Rank= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    telecom_Upgrades_total_Target= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    telecom_Upgrades_total_Achieved= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    telecom_Ach_to_Target= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    telecom_Ach_to_First= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Weight_of_telecom_Target= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Weight_of_telecom_Ach= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Weight_of_telecom_Rollout= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    telecom_Upgrades_Score= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    telecom_Upgrades_Rank= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Civil_Enhancement_total_Target= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Civil_Enhancement_total_Achieved= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Weight_of_Civil_Rank= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Civil_Enhancement_Ach_to_First_30= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Civil_Enhancement_Score= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Civil_Enhancement_Rank= models.DecimalField( max_digits=5, decimal_places=2, default=0)


    def __str__(self):
        return self.Contractor

    
class RankTabCivil(models.Model):

        Contractor = models.OneToOneField(Contractor_DB,on_delete=models.CASCADE)



        Rollout_Cairo_Civil_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Giza_Civil_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Delta_Civil_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Alex_Civil_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Upper_Civil_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Cairo_Civil_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Giza_Civil_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Delta_Civil_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Alex_Civil_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Upper_Civil_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Imp_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Acceptance_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        H_S_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Cost_Control_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Civil_Enhancement_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        

        Rollout_Cairo_Civil_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Giza_Civil_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Delta_Civil_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Alex_Civil_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Upper_Civil_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Cairo_Civil_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Giza_Civil_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Delta_Civil_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Alex_Civil_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Upper_Civil_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Imp_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Acceptance_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        H_S_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Cost_Control_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Civil_Enhancement_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)



        Rollout_Cairo_Civil_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Giza_Civil_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Delta_Civil_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Alex_Civil_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Upper_Civil_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Cairo_Civil_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Giza_Civil_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Delta_Civil_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Alex_Civil_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Upper_Civil_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Imp_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Acceptance_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        H_S_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Cost_Control_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Civil_Enhancement_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)



        Rollout_Cairo_Civil_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Giza_Civil_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Delta_Civil_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Alex_Civil_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Upper_Civil_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Cairo_Civil_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Giza_Civil_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Delta_Civil_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Alex_Civil_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Upper_Civil_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Imp_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Acceptance_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        H_S_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Cost_Control_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Civil_Enhancement_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)



        def __str__(self):
            return self.Contractor

class RankingTab_Telecom(models.Model):
        Contractor = models.OneToOneField(Contractor_DB,on_delete=models.CASCADE)



        Rollout_Cairo_Telecom_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Giza_Telecom_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Delta_Telecom_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Alex_Telecom_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Upper_Telecom_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Cairo_Telecom_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Giza_Telecom_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Delta_Telecom_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Alex_Telecom_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Upper_Telecom_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Imp_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Acceptance_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        H_S_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Cost_Control_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Telecom_Enhancement_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        

        Rollout_Cairo_Telecom_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Giza_Telecom_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Delta_Telecom_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Alex_Telecom_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Upper_Telecom_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Cairo_Telecom_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Giza_Telecom_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Delta_Telecom_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Alex_Telecom_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Upper_Telecom_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Imp_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Acceptance_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        H_S_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Cost_Control_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Telecom_Enhancement_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)


        Rollout_Cairo_Telecom_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Giza_Telecom_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Delta_Telecom_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Alex_Telecom_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Upper_Telecom_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Cairo_Telecom_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Giza_Telecom_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Delta_Telecom_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Alex_Telecom_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Upper_Telecom_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Imp_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Acceptance_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        H_S_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Cost_Control_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Telecom_Enhancement_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)


        Rollout_Cairo_Telecom_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Giza_Telecom_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Delta_Telecom_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Alex_Telecom_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Rollout_Upper_Telecom_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Cairo_Telecom_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Giza_Telecom_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Delta_Telecom_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Alex_Telecom_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Imp_Upper_Telecom_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        IBS_Imp_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Acceptance_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        H_S_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Cost_Control_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)
        Telecom_Enhancement_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)



        def __str__(self):
            return self.Contractor

class RankingTabPower(models.Model):
    Contractor = models.OneToOneField(Contractor_DB,on_delete=models.CASCADE)




    Acceptance_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Acceptance_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Acceptance_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Acceptance_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)



    def __str__(self):
        return self.Contractor

class FinalTab_Civil(models.Model):
    Contractor = models.OneToOneField(Contractor_DB,on_delete=models.CASCADE)



    Technical_Competence_10= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Acceptance_10= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Financial_Invoicing_10= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Health_Safety_10= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Prod_Rollout_40= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Prod_Civil_Upgrades_10= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Prod_Civil_enhancement_10= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Total_Q1= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Total_Q2= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Total_Q3= models.DecimalField( max_digits=5, decimal_places=2, default=0)
    Total_Q4= models.DecimalField( max_digits=5, decimal_places=2, default=0)


    def __str__(self):
        return self.Contractor
        
