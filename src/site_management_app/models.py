from django.db import models

# Create your models here.
class site_management_db(models.Model):
    yes='yes'
    no='no'
    yes_no_choice=[(yes,'Yes'),(no,'No')]
    site_id                 = models.CharField(blank=False,max_length=30)
    Last_Rent               =models.FloatField(null=True, blank=True, default=None)
    System_Start_Date       =models.DateField(blank=True, null=True)
    System_End_Date         =models.DateField(blank=True, null=True)
    Calc_From               =models.DateField(blank=True, null=True)
    Calc_To                 =models.DateField(blank=True, null=True)
    Access_Status           =models.CharField(blank=False,max_length=30)
    problematic_owner       =models.CharField(blank=False,max_length=30)
    health_safety           = models.CharField(max_length=30,
                                              choices = yes_no_choice,
                                              blank=False, null=True)
    tech_issue              = models.CharField(max_length=30,
                                              choices = yes_no_choice,
                                              blank=False, null=True)
    remove_order            = models.CharField(max_length=30,
                                              choices = yes_no_choice,
                                              blank=False, null=True)
    legal                   = models.CharField(max_length=30,
                                              choices = yes_no_choice,
                                              blank=False, null=True)
# define functions
    def __str__(self):
        return self.site_id


class cluster_average(models.Model):
    site_id = models.CharField(blank=False, max_length=30)
    cl_avg_key=models.CharField(blank=False, max_length=70)
    cl_avg_rent=models.DecimalField(max_digits=10,null=True, blank=True, default=None,decimal_places=2)
    def __str__(self):
        return self.site_id