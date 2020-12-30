from django.contrib import admin

# Register your models here.
from .models import pki_record,pki_source
# Register your models here.
class pki_record_admin(admin.ModelAdmin):
    list_display = ['__str__','vendor','serial']
    class Meta:
        model=pki_record
admin.site.register(pki_record,pki_record_admin)
admin.site.register(pki_source)