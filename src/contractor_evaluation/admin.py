from django.contrib import admin
from .models import Contractor_DB,rollout_pool,rollout_db,telecom_civil_db,Ranking_db,RankTabCivil\
    ,RankingTab_Telecom,RankingTabPower,FinalTab_Civil
# Register your models here.
admin.site.register(Contractor_DB)
admin.site.register(rollout_pool)
admin.site.register(rollout_db)
admin.site.register(telecom_civil_db)
admin.site.register(Ranking_db)
admin.site.register(RankingTab_Telecom)
admin.site.register(RankingTabPower)
admin.site.register(FinalTab_Civil)
admin.site.register(RankTabCivil)
