from django.db import models

# Create your models here.
class power_info(models.Model):
    Site_Name = models.CharField(blank=False, max_length=100)
    site_id = models.CharField(blank=False, max_length=30)
    Site_Vendor =models.CharField(blank=False, max_length=30)
    Site_Region =models.CharField(blank=False, max_length=30)
    Site_Type =models.CharField(blank=False, max_length=30)
    Site_State =models.CharField(blank=False, max_length=30)
    Position =models.CharField(blank=False, max_length=30)
    Governate =models.CharField(blank=False, max_length=30)
    Cabients_Type =models.CharField(blank=False, max_length=30)
    Cabinet_Num =models.CharField(blank=False, max_length=30)
    Cabinet_Activity =models.CharField(blank=False, max_length=30)
    System_Voltage =models.IntegerField(default=0)
    Rectifier_Type =models.CharField(blank=False, max_length=30)
    Rect_Count =models.IntegerField(default=0)
    Needed_Rectifiers =models.IntegerField(default=0)
    Battery_Type=models.CharField(blank=False, max_length=30)
    Bat_Count=models.IntegerField(default=0)
    Needed_Batteries=models.IntegerField(default=0)
    Power_Cabinet=models.CharField(blank=False, max_length=30)
    Power_Conumption=models.DecimalField(null=True, blank=True, default=None,max_digits=20,decimal_places=2)
    Generated_Power=models.DecimalField(null=True, blank=True, default=None,max_digits=20,decimal_places=2)
    FC_Comp_Name=models.CharField(blank=False, max_length=30)
    FC_Comp_Count=models.IntegerField(default=0)
    Battery_cabinet=models.CharField(blank=False, max_length=30)
    Bat_Cab_Count=models.IntegerField(default=0)

# define functions
    def __str__(self):
        return self.site_id





class civil_info(models.Model):
    site_id = models.CharField(blank=False, max_length=30)
    Name= models.CharField(blank=False, max_length=100)
    Area= models.CharField(blank=False, max_length=30)
    Requester= models.CharField(blank=False, max_length=30)
    Consultant_name= models.CharField(blank=False, max_length=30)
    Request_Date= models.DateField(blank=True, null=True)
    New_requirement= models.TextField(blank=False)
    new_requirement_details= models.TextField(blank=False)
    attached_mail= models.CharField(blank=False, max_length=30)
    Status= models.CharField(blank=False, max_length=30)
    EIC= models.CharField(blank=False, max_length=30)
    Feed_back= models.DateField(blank=True, null=True)
    Project_Name= models.CharField(blank=False, max_length=30)
    Site_Status= models.CharField(blank=False, max_length=30)
    RT_GF= models.CharField(blank=False, max_length=30)
    ST_Type= models.CharField(blank=False, max_length=30)
    Tower_Type= models.CharField(blank=False, max_length=30)
    Height= models.CharField(blank=False, max_length=30)
    Tower_body= models.CharField(blank=False, max_length=30)
    Grillage= models.CharField(blank=False, max_length=30)
    Anchoring= models.CharField(blank=False, max_length=30)
    Building= models.CharField(blank=False, max_length=30)
    Consultant_recommendations= models.TextField(blank=False)
    Action_Taken= models.CharField(blank=False, max_length=30)
    Remarks= models.TextField(blank=False, max_length=30)

    # define functions
    def __str__(self):
        return self.site_id


