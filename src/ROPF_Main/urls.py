"""ROPF_Main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import admin_page
from pki_interaction_app.views import export_requested,export_all,pki_upload,source_export_all,pki_test
from site_management_app.views import contract_renegotiation,site_continuity_risk
from ropf_auth.views import login_page,welcome,logout_page,auth_error_page,new_pass
from site_history_app.views import site_hisory,civil_info_page,power_info_page,site_info_page
from nfm_rca.views import nfm_rca
from contractor_evaluation.views import cont_eva
from civil_technical_office.views import civil_fn
from .views import under_construction

urlpatterns = [


    path('admin/', admin.site.urls),
    path('', login_page),
    path('under_construction/', under_construction),
    path('welcome/',welcome),
    path('logout/',logout_page),
    path('auth_error/',auth_error_page),
    path('new_password/',new_pass),
    path('export/requested/', export_requested,name='export_excel'),
    path('export/all/', export_all,name='export_excel'),
    path('pki_test/', pki_test),
    path('pki/', pki_upload),
    path('contract_renegotiation/', contract_renegotiation),
    path('site_continuity_risk/', site_continuity_risk),
    path('site_history/', site_info_page),
    path('civil_info/', civil_info_page),
    path('power_info/', power_info_page),
    path('ropf_admin/',admin_page),
    path('nfm_crca/',nfm_rca),
    path('civil_tech/', civil_fn),
    path('cont_eva/', cont_eva),
    re_path(r'^celery-progress/', include('celery_progress.urls')),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
