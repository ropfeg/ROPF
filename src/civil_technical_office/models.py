from django.db import models
from django.db.models import Max
import re

# Create your models here.

class SiteData(models.Model):
    
    #UserInput
    site_id = models.CharField(max_length=30)
    consultant_name = models.CharField(max_length=30, blank=True, null=True)
    requester_dept = models.CharField(max_length=30, blank=True, null=True)
    request_date = models.DateField(blank=True, null=True)
    new_requirement = models.TextField(blank=True, null=True)
    last_visit = models.DateField(blank=True, null=True, default="")
    status = models.CharField(max_length=30,blank=True, null=True,choices=(('in-progress','in-progress'),('done','done')))
    feedback = models.DateField(blank=True, null=True, default="")
    requester = models.CharField(max_length=30, blank=True, null=True)
    remarks = models.CharField(max_length=256, blank=True, null=True)
    mail_name = models.CharField(max_length=30, blank=True, null=True)
    project_name = models.CharField(max_length=30, blank=True, null=True)
    site_case = models.CharField(max_length=30,blank=True, null=True)
    building = models.CharField(max_length=30,blank=True, null=True)
    max_rating_in = models.CharField(max_length=30, blank=True, null=True)
    max_rating_per = models.CharField(max_length=30,blank=True, null=True)
    consultant_recommendations = models.CharField(max_length=30, blank=True, null=True)
    action_taken = models.CharField(max_length=30,blank=True, null=True)
    star_site = models.CharField(max_length=30, blank=True, null=True)
    employee_id = models.CharField(max_length=30, blank=True, null=True)
    #Hidden fields
    last_modfied_date = models.DateTimeField(auto_now=True)
    last_modfied_user = models.CharField(max_length=30, blank=True, null=True)

    #Auto
    in_progress_date = models.CharField(max_length=30, blank=True, null=True)
    done_date = models.CharField(max_length=30, blank=True, null=True)
    region= models.CharField(max_length=30, blank=True, null=True)
    site_type= models.CharField(max_length=30, blank=True, null=True)
    structure_type= models.CharField(max_length=30, blank=True, null=True)
    height=models.CharField(max_length=30, blank=True, null=True)


    wo_id = models.CharField(primary_key=True, editable=False, max_length=10)
    
    def __str__(self):
        return self.site_id

    def save(self, **kwargs):
        if not self.wo_id:
            max_wo_id= SiteData.objects.aggregate(Max('wo_id'))['wo_id__max']
            new_wo_id = int(re.findall('\d+',max_wo_id)[0])+1
            self.wo_id = f'WO{str(new_wo_id).zfill(6)}'
        super().save(*kwargs)


    
