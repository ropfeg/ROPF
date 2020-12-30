from django.contrib import admin

# Register your models here.
from .models import power_info,civil_info
class power_info_admin(admin.ModelAdmin):
    list_display = ['__str__']
    class Meta:
        model=power_info
admin.site.register(power_info,power_info_admin)
admin.site.register(civil_info)