from django.db import models

# Create your models here.
class general_info(models.Model):
    Alex = "Alex"
    Cairo = "Cairo"
    Delta = "Delta"
    Giza = "Giza"
    Upper = "Upper"
    region_choice = [(Alex,"Alex"),(Cairo,"Cairo"),(Delta,"Delta"),(Giza,"Giza"),(Upper,"Upper")]
    yes = 'yes'
    no = 'no'
    yes_no_choice = [(yes, 'Yes'), (no, 'No')]
    site_id=models.CharField(blank=False, max_length=30)
    option=models.CharField(blank=False, max_length=1)
    region=models.CharField(max_length=30,
                            choices=region_choice,
                            blank=False, null=True)
    sub_region=models.CharField(blank=False, max_length=30)
    longitude=models.FloatField(null=True, blank=True, default=None)
    latitude=models.FloatField(null=True, blank=True, default=None)
    site_type=models.CharField(blank=False, max_length=30)
    height=models.FloatField(null=True, blank=True, default=None)
    structure_type=models.CharField(blank=False, max_length=30)
    cluster_avg=models.FloatField(null=True, blank=True, default=None)
    guarded_status = models.CharField(max_length=30,
                              choices=yes_no_choice,
                              blank=False, null=True,default=no)
    north_sinai_status= models.CharField(max_length=30,
                              choices=yes_no_choice,
                              blank=False, null=True,default=no)
    VF_CP="VF_CP"
    VF_Gen="VF_Gen"
    VF_Hybrid="VF_Hybrid"
    ET_CP= "ET_CP"
    OR_CP= "OR_CP"
    TE_CP= "TE_CP"
    VF_PC= "VF_PC"
    OR_Gen= "OR_Gen"
    ET_Gen= "ET_Gen"
    TE_Gen= "TE_Gen"
    VF_Solar= "VF_Solar"
    
    power_source_choice= [(VF_CP,"VF_CP"),(VF_Gen,"VF_Gen"),(VF_Hybrid,"VF_Hybrid"),
                          (ET_CP, "ET_CP"),(OR_CP, "OR_CP"),(TE_CP, "TE_CP"),
                          (VF_PC, "VF_PC"),(OR_Gen, "OR_Gen"),(ET_Gen, "ET_Gen"),
                          (TE_Gen, "TE_Gen"),(VF_Solar, "VF_Solar"),
                          ]
    power_source_status = models.CharField(max_length=30,
                                          choices=power_source_choice,
                                          blank=False, null=True)
    def __str__(self):
        return self.site_id


class radio_info(models.Model):
    Medium="Medium"
    Critical="Critical"
    High="High"
    Very_Low="Very Low"
    Low="Low"
    Not_Ranked="Not Ranked"
    rank_choice=[(Medium,"Medium"),(Critical,"Critical"),(High,"High"),(Very_Low,"Very Low"),(Low,"Low"),(Not_Ranked,"Not Ranked")]

    site_id = models.CharField(blank=False, max_length=30)
    rank    =models.CharField(max_length=30,
                            choices=rank_choice,
                            blank=False, null=True)
    def __str__(self):
        return self.site_id
class tx_info(models.Model):
    site_id = models.CharField(blank=False, max_length=30)
    cascaded_sites = models.IntegerField(default=0)
    def __str__(self):
        return self.site_id