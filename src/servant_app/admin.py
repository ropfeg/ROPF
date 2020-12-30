from django.contrib import admin

# Register your models here.
from .models import general_info,radio_info,tx_info
# Register your models here.

admin.site.register(general_info)
admin.site.register(radio_info)
admin.site.register(tx_info)