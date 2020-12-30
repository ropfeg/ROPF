from django.contrib import admin
from .models import site_management_db,cluster_average
# Register your models here.
admin.site.register(site_management_db)
admin.site.register(cluster_average)