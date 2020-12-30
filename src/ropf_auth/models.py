from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # define vendor list
    radio = 'radio'
    regional_operations = 'Regional_operation'
    service_management = 'service_management'
    department_choice = [(regional_operations, 'Regional_Operations'), (radio, 'Radio'),
                         (service_management, 'service_management')]
    # sub department and region
    all="All"
    cairo = 'Cairo'
    giza = 'Giza'
    delta = 'Delta'
    alex = 'Alexandria'
    Giza_Alex_Region="Giza_Alex_Region"
    upper = 'Upper-Red Sea and Sinai'
    gov='governance'
    Acceptance="Acceptance"
    sub_dep_choice = [(cairo, 'Cairo_Region'), (giza, 'Giza_Region'), (delta, 'Delta_Region'), (alex, 'Alexandria_Region'),
                      (upper, 'Upper_Region'),(gov,'Govrernance'),(Acceptance,"Acceptance"),(Giza_Alex_Region,"Giza_Alex_Region"),
                      (regional_operations, 'Regional_Operations')]

    region_choice =[(cairo, 'Cairo'), (giza, 'Giza'), (delta, 'Delta'), (alex, 'Alexandria'),
                    (upper, 'Upper-Red Sea and Sinai'),(Giza_Alex_Region,"Giza_Alex_Region"),(all,'All')]
    # define teams
    implementation = "Implementation"
    rollout = "Rollout"
    nfm = "nfm"
    dev = "Development"
    sm="SiteMnanagement"
    Environmental="Environmental"
    team_choice = [(implementation, "Implementation"), (rollout, "Rollout"), (dev, "Development"),
                   (Environmental,"Environmental"),(sm,"SiteMnanagement"),(cairo, 'Cairo_Region'),
                   (giza, 'Giza_Region'), (delta, 'Delta_Region'), (alex, 'Alexandria_Region'),
                    (upper, 'Upper_Region'),(gov,'Govrernance'),(Acceptance,"Acceptance"),
                   (Giza_Alex_Region,"Giza_Alex_Region"),(regional_operations, 'Regional_Operations')]
    # define user_type
    department = models.CharField(max_length=30,
                                  choices=department_choice,
                                  blank=False, null=True)
    sub_dep = models.CharField(max_length=30,
                              choices=sub_dep_choice,
                               blank=False, null=True)
    user_region = models.CharField(max_length=30,
                               choices=region_choice,
                               blank=False, null=True)
    team = models.CharField(max_length=30,
                            choices=team_choice,
                            blank=False, null=True)

    admin = models.BooleanField(default=False)  # admin
    image =models.FileField(upload_to='ropf_auth/',null=True,blank=True)

    def __str__(self):
        return self.user.username



# class Super_User(models.Model):
#     user= models.OneToOneField(User, on_delete=models.CASCADE)
#
# class HOD(models.Model):
#     user= models.OneToOneField(User, on_delete=models.CASCADE)
#
# class Manager(models.Model):
#     user= models.OneToOneField(User, on_delete=models.CASCADE)
#     pki = models.BooleanField(default=False)
#     site_history=models.BooleanField(default=False)
#     contract_renegotiation=models.BooleanField(default=False)
#     site_continuity_risk=models.BooleanField(default=False)
#
# class SPOC(models.Model):
#     user= models.OneToOneField(User, on_delete=models.CASCADE)
#     pki = models.BooleanField(default=False)
#     site_history=models.BooleanField(default=False)
#     contract_renegotiation=models.BooleanField(default=False)
#     site_continuity_risk=models.BooleanField(default=False)
#

class user_privilege(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    read='r'
    read_write='cr'
    cru = 'cru'
    crud='crud'
    no="no"
    usertype_choices=[(read,'r'),(read_write,'cr'),(cru,'cru'),(crud,'crud'),(no,'no')]

    pki = models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    site_history=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    contract_renegotiation=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    site_continuity_risk=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    dashboard=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    query=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    technical_Plan=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    integration_Quota=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    smart_check_list=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    contractor_evaluation=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    contractor_allocation=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    field_planning=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    rca_acceptance=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    rca_nfm=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    civil_technical_office=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    unified_pwr_db=models.CharField(max_length=30,choices=usertype_choices,blank=False, null=True,default=no)
    def __str__(self):
        return self.user.username

class User(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)