from django.contrib import admin
# from .models import UserProfile,Super_User,SPOC,User,Manager,HOD
from .models import UserProfile,user_privilege
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(user_privilege)
# admin.site.register(Super_User)
# admin.site.register(SPOC)
# admin.site.register(Manager)
# admin.site.register(HOD)
