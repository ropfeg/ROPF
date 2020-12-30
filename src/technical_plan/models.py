from django.db import models

# Create your models here.
import datetime

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year.__int__()

class tp_name(models.Model):


    tp_name = models.CharField(blank=False,max_length=30)
    year    = models.IntegerField( default=current_year)
    fy_year =models.CharField(blank=False,max_length=7,null=True)
    version = models.IntegerField()


class tp_details(models.Model):
    start_date_default = datetime.date(datetime.date.today().year.__int__(), 4, 1)
    end_date_default = datetime.date(datetime.date.today().year.__int__()+1, 3, 31)

    tp_name = models.ForeignKey(tp_name, on_delete=models.CASCADE)
    Stream = models.CharField(blank=False, max_length=30, null=True)
    Alex_ER         =models.IntegerField( default=0)
    Alex_HU         =models.IntegerField( default=0)
    Cairo_ER        =models.IntegerField( default=0)
    Cairo_HU        =models.IntegerField( default=0)
    Delta_ER        =models.IntegerField( default=0)
    Delta_HU        =models.IntegerField( default=0)
    Giza_ER         =models.IntegerField( default=0)
    Giza_HU         =models.IntegerField( default=0)
    Canal_HU        =models.IntegerField( default=0)
    Upper_HU        =models.IntegerField( default=0)
    G_Cairo_ER = models.IntegerField(default=0)
    G_Cairo_HU = models.IntegerField(default=0)
    Total_Upper_HU  =models.IntegerField( default=0)
    Total_ER        =models.IntegerField( default=0)
    Total_HU        =models.IntegerField( default=0)
    Total_plans_V3  =models.IntegerField( default=0)
    Integ_Weights   =models.IntegerField( default=0)
    Total_ER_weighted   =models.IntegerField( default=0)
    Total_HU_weighted   =models.IntegerField( default=0)
    Total_Weighted_V3   =models.IntegerField( default=0)
    Start_date          =models.DateField( default=start_date_default)
    End_date            =models.DateField( default=end_date_default)
    Stream_life_time    =models.IntegerField( default=12)

class acheived(models.Model):

    Stream = models.ForeignKey(tp_details, on_delete=models.CASCADE)



class assumption_phasing(models.Model):

    Stream = models.ForeignKey(tp_details, on_delete=models.CASCADE)
    # apr_eric
    # apr_hu
    #

class region_phasing(models.Model):

    Stream = models.ForeignKey(tp_details, on_delete=models.CASCADE)