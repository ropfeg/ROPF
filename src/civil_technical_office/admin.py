from django.contrib import admin
from civil_technical_office.models import SiteData
import uuid 

# Register your models here.
#
# class SiteDataAdmin(admin.ModelAdmin):
#     readonly_fields=('wo_id','last_modifed','updated_at')

admin.site.register(SiteData)