from django.db import models

# Create your models here.
from django.db import models

# Create your models here.




class pki_record(models.Model):


#define vendor list
    huawei = 'huawei'
    ericsson = 'ericsson'
    vendor_choice = [(huawei,'huawei'),(ericsson,'ericsson')]

# define Region list
    Alex = "Alex"
    Cairo = "Cairo"
    Delta = "Delta"
    Giza = "Giza"
    Upper = "Upper"
    L1 = "L1"
    region_choice = [(Alex,"Alex"),(Cairo,"Cairo"),(Delta,"Delta"),(Giza,"Giza"),(Upper,"Upper"),(L1,"L1")]

# define Function list
    Imp = "Imp"
    Rollout = "Rollout"
    IBS = "IBS"

    function_choice = [(Imp,"Imp"),(Rollout,"Rollout"),(IBS,"IBS"),(L1,"L1")]

# define pki_status_1 list
    Exists = "Exists"                           # in case serial added to pki
    Request_in_progress = "Request_in_progress" #in case serial not exist in source db
    Requested = "Requested"                     #in case list "request in-progress" exported
    pki_status1_choice = [(Exists, "Exists"), (Request_in_progress, "Request In-Progress"), (Requested, "Requested")]

# define pki_status_1 list
    Removed = "Removed"                         #in case it doesn't esist in source db but have in (pki status 1) --> exists
    pki_status2_choice = [(Removed, "Removed"), (Exists, "Exist")]

# define CRQ_Status list
    need_crq = "Need CRQ"                      # in case crq # is empty
    rfa = "RFA"                                # in case crq # exist and serial not exist
    done = "Done"                              # in case serial exist
    crq_status_choice = [(need_crq, "Need CRQ"), (rfa, "RFA"), (done, "Done")]
# define request_type List
    add="Add"
    remove="Remove"
    request_type_choice=[(add,"Add"),(remove,"Remove")]

    site_id                 = models.CharField(blank=False,max_length=30)
    vendor                  = models.CharField(max_length=30,
                                              choices = vendor_choice,
                                              blank=False, null=True)
    serial                  = models.CharField(blank=False,max_length=30)
    activity                = models.CharField(blank=False,max_length=30)
    region                  = models.CharField(max_length=30,
                                              choices=region_choice,
                                              blank=False, null=True)
    function                = models.CharField(max_length=30,
                                              choices=function_choice,
                                              blank=False, null=True)
    pki_status1             = models.CharField(max_length=30,
                                              choices=pki_status1_choice,
                                              blank=True, null=True
                                               ,default="Requested")
    pki_status2             = models.CharField(max_length=30,
                                              choices=pki_status2_choice,
                                              blank=True, null=True)
    crq_status              = models.CharField(max_length=30,
                                              choices=crq_status_choice,
                                              blank=True, null=True)
    crq_no                  = models.CharField(max_length=30,blank=True)
    batch_no                = models.IntegerField(default=0,)
    username                = models.CharField(max_length=30,blank=True)
    collection_date         = models.DateField(blank=True, null=True)
    admin_export_date       = models.DateField(blank=True, null=True)
    crq_creation_date       = models.DateField(blank=True, null=True)
    crq_executation_date    = models.DateField(blank=True, null=True)
    export_collect          = models.IntegerField(default=0)
    create_export           = models.IntegerField(default=0)
    execute_create          = models.IntegerField(default=0)
    total_issue_time        = models.IntegerField(default=0)
    pki_comment             = models.TextField(blank=True, null=True)
    req_type                = models.CharField(max_length=30,
                                              choices=request_type_choice,
                                              blank=True, null=True)
# define functions
    def __str__(self):
        return self.site_id





class pki_source(models.Model):

    serials                 = models.CharField(blank=False, max_length=30)
    vendor                  = models.CharField(blank=False, max_length=30)


    def __str__(self):
        return self.serials