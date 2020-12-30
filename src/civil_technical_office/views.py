from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from civil_technical_office.models import SiteData
from servant_app.models import general_info
from django.http import HttpResponse
from django.db.models import Max
from ropf_auth.models import user_privilege,UserProfile
import csv
from itertools import chain


def migrate_from_csv():
    import sqlite3
    import pandas as pd
    cnx = sqlite3.connect('C:\\path\\to\\database')
    csv_data = pd.read_csv("C:\\path\\to\\csv")
    csv_data.to_sql(name='civil_technical_office_sitedata', con=cnx, if_exists='append', index=False)
    cnx.commit()
    cnx.close()



# Create your views here.

@login_required(login_url='/')
def civil_fn(request):
    context={}
    user_name = request.user.username
    user_id = request.user.id
    # print(user_id)
    context = {"username":user_name}
    # --------- start auth ------------
    if user_privilege.objects.filter(user_id=user_id).exists():

        if user_privilege.objects.get(user_id=user_id).rca_nfm == "no":
            return redirect("/auth_error/")
        else:
            context.update({
                'userprivileges':user_privilege.objects.get(user_id=user_id).rca_nfm,
                'read': ['r', 'cr','cru', 'crud'],
                'read_write': ['cr', 'cru','crud'],
                'cru':['cru', 'crud'],
                'crud':['crud']
            })
    if UserProfile.objects.filter(user_id=user_id).exists():

        userprofile = UserProfile.objects.get(user_id=user_id)
        # print(userprofile)
        print(request.POST)
        # print(userprofile.image.url)
        context.update({
                    # "avatar":userprofile.image.url

        })

    # ----------- end auth ------------

    #Search is now functional using both site and wo_id (validations/errors are done)
    #if no servant app info (fixed, handled with nested try)
    if request.method == 'POST' and 'site_search' in request.POST:

        if request.POST.get('wo_id'):
            context.update({'request_id':"Search"}) 
            try:
                searched_wo_id= request.POST.get('wo_id')
                results = SiteData.objects.get(wo_id=searched_wo_id , status="done")
                inprogress_date_str_info = datetime.strftime(datetime.strptime(results.in_progress_date, '%Y-%m-%d %H:%M:%S.%f'), '%Y-%m-%d %H:%M:%S')
                done_date_str_info = datetime.strftime(datetime.strptime(results.done_date, '%Y-%m-%d %H:%M:%S.%f'), '%Y-%m-%d %H:%M:%S')
                
                try:
                    servant_app_results = general_info.objects.get(site_id=results.site_id)
                    context.update({"servant_app_results":servant_app_results})
                except ObjectDoesNotExist:
                    no_servantapp="no servantapp"

                context.update({"results":results})
                context.update({"inprogress_date_str_info":inprogress_date_str_info})
                context.update({"done_date_str_info":done_date_str_info})
                context.update({'delete':"exist"})

            except ObjectDoesNotExist:
                wo_id_existence_error = "No done request with this wo id exists"
                context.update({"wrong_wo_id":"yes"})
            
        elif request.POST.get('site_id'):
            context.update({'search_id':"Search"})
            try:
                searched_site_id= request.POST.get('site_id')
                results = SiteData.objects.filter(site_id=searched_site_id , status="done").latest('done_date')
                inprogress_date_str_info = datetime.strftime(datetime.strptime(results.in_progress_date, '%Y-%m-%d %H:%M:%S.%f'), '%Y-%m-%d %H:%M:%S')
                done_date_str_info = datetime.strftime(datetime.strptime(results.done_date, '%Y-%m-%d %H:%M:%S.%f'), '%Y-%m-%d %H:%M:%S')
                
                try:
                    servant_app_results = general_info.objects.get(site_id=searched_site_id)
                    context.update({"servant_app_results":servant_app_results})
                except ObjectDoesNotExist:
                     no_servantapp="no servantapp"

                context.update({"results":results})
                context.update({"inprogress_date_str_info":inprogress_date_str_info})
                context.update({"done_date_str_info":done_date_str_info})
                context.update({'extract':"exist"})

            
            except ObjectDoesNotExist:
                site_id_existence_error = "No done request with this site id exists"
                context.update({"search_for_done":"no"})
        else:
            site_and_wo_id_existence_error = "Please provide at least one of the given search criterias to search"
            context.update({"site_and_wo_id_existence_error":site_and_wo_id_existence_error})
    
        return render(request,"civil_technical_office/civil_tech.html",context)

    #functioning but waiting for tawfik for new functionality (only site_id no wo_id)
    elif request.method == 'POST' and 'site_search_update' in request.POST:
        context = {}
        context.update({"Searched":'Yes'})
        try:
            searched_site_id= request.POST.get('update_search_site_id')
            update_results = SiteData.objects.filter(site_id=searched_site_id).latest('in_progress_date')

            request_date_str_update = datetime.strftime(update_results.request_date, '%Y-%m-%d')

            if update_results.feedback != None: 
                feedback_date_str_update = datetime.strftime(update_results.feedback, '%Y-%m-%d')
                context.update({"feedback_date_str_update":feedback_date_str_update})
            if update_results.last_visit != None: 
                last_visit_date_str_update = datetime.strftime(update_results.last_visit, '%Y-%m-%d')
                context.update({"last_visit_date_str_update":last_visit_date_str_update})

            inprogress_date_str_update = datetime.strftime(datetime.strptime(update_results.in_progress_date, '%Y-%m-%d %H:%M:%S.%f'), '%Y-%m-%d %H:%M:%S')
            if not update_results.status == "done":
                
                context.update({"update_results":update_results})
                context.update({"request_date_str_update":request_date_str_update})
                context.update({"inprogress_date_str_update":inprogress_date_str_update})

                try:
                    update_servant_app_results = general_info.objects.get(site_id=searched_site_id)
                    context.update({"update_servant_app_results":update_servant_app_results})
                except ObjectDoesNotExist:
                    no_servantapp="no servantapp"
                return render(request,"civil_technical_office/civil_tech.html",context)
            else:
                already_done_validation = "Can't edit this record as status has been marked as done"
                context.update({"search_in_progress":"no"})
                return render(request,"civil_technical_office/civil_tech.html",context)
        #should be seperate for wo_id and site_id
        except ObjectDoesNotExist:
            existence_error = "wala ay 7aga"
            context.update({"site_exist":"no"})
            return render(request,"civil_technical_office/civil_tech.html",context)

    #add is now functional and checks for existing in-progress (Validations/success are done)
    elif request.method == 'POST' and 'add_new_site' in request.POST:
        context = {}


        filtered_site_data= SiteData.objects.filter(site_id=request.POST.get('site_id'), status="in-progress")

        if not filtered_site_data:

            civil_request = SiteData()

            civil_request.site_id= request.POST.get('site_id')
            civil_request.consultant_name= request.POST.get('consultant_name')
            civil_request.requester_dept =request.POST.get('requester_dept')
            civil_request.request_date= request.POST.get('request_date')
            civil_request.new_requirement= request.POST.get('new_requirement')

            if request.POST.get('last_visit') == "":
                civil_request.last_visit= None
            else:
                civil_request.last_visit= request.POST.get('last_visit')

            if request.POST.get('feedback') == "":
                civil_request.feedback= None
            else:
                civil_request.feedback= request.POST.get('feedback')

            civil_request.status = request.POST.get('status')
            civil_request.requester =request.POST.get('requester')
            civil_request.remarks= request.POST.get('remarks')
            civil_request.mail_name= request.POST.get('mail_name')
            civil_request.project_name= request.POST.get('project_name')
            civil_request.site_case = request.POST.get('site_case')
            civil_request.building = request.POST.get('building')
            civil_request.max_rating_in=request.POST.get('max_rating_in')
            civil_request.consultant_recommendations= request.POST.get('consultant_recommendations')
            civil_request.action_taken= request.POST.get('action_taken')
            civil_request.star_site= request.POST.get('star_site')
            civil_request.max_rating_per= request.POST.get('max_rating_per')
            try:
                print(general_info.objects.filter(site_id=request.POST.get('site_id'))[0].region)
                civil_request.region= general_info.objects.filter(site_id=request.POST.get('site_id'))[0].region
                civil_request.site_type = general_info.objects.filter(site_id=request.POST.get('site_id'))[0].site_type
                civil_request.structure_type = general_info.objects.filter(site_id=request.POST.get('site_id'))[0].structure_type
                civil_request.height = general_info.objects.filter(site_id=request.POST.get('site_id'))[0].height



            except:
                civil_request.region=None
                civil_request.site_type=None
                civil_request.structure_type=None
                civil_request.height=None

            civil_request.employee_id = request.user.username
            civil_request.in_progress_date = datetime.now()
            civil_request.last_modfied_date = datetime.now()
            civil_request.last_modfied_user = request.user.username
            civil_request.save()     

            add_success = f'Request added successfully with work ID {civil_request.wo_id}, please use this Ref ID for later operations'
            context.update({"site_add": "yes"})
            
        else:      
            already_inprogress_validation= "An In-Progress request for this site already exits"        
            context.update({"already_inprogress_validation": already_inprogress_validation})

        return render(request,"civil_technical_office/civil_tech.html",context)    
    
    elif request.method == 'POST' and 'update_new_site' in request.POST:
        context = {}
        context.update({"Searched":'Yes'})
        searched_site_id= request.POST.get('update_site_id_hidden')

        civil_request = SiteData.objects.filter(site_id=searched_site_id).latest('in_progress_date')

        if str(request.POST.get('update_status')) == "done":
            civil_request.done_date = datetime.now()

        civil_request.consultant_name= request.POST.get('update_consultant_name')
        civil_request.requester_dept =request.POST.get('update_requester_dept')
        civil_request.request_date= request.POST.get('update_request_date')
        civil_request.new_requirement= request.POST.get('update_new_requirement')
        civil_request.last_visit= request.POST.get('update_last_visit')
        civil_request.status = request.POST.get('update_status')
        civil_request.feedback= request.POST.get('update_feedback')
        civil_request.requester =request.POST.get('update_requester')
        civil_request.remarks= request.POST.get('update_remarks')
        civil_request.mail_name= request.POST.get('update_mail_name')
        civil_request.project_name= request.POST.get('update_project_name')
        civil_request.site_case = request.POST.get('update_site_case')
        civil_request.building = request.POST.get('update_building')
        civil_request.max_rating_in=request.POST.get('update_max_rating_in')
        civil_request.max_rating_per= request.POST.get('update_max_rating_per')
        civil_request.consultant_recommendations= request.POST.get('update_consultant_recommendations')
        civil_request.action_taken= request.POST.get('update_action_taken')
        civil_request.star_site= request.POST.get('update_star_site')
        civil_request.last_modfied_date = datetime.now()
        civil_request.last_modfied_user = request.user.username

        civil_request.save()

        update_success = "Request updated successfully"
        context.update({"site_update": "yes"})
        return render(request,"civil_technical_office/civil_tech.html",context)
    #Delete is now functional using wo_id
    elif request.method == 'POST' and 'delete_site' in request.POST:

        searched_wo_id= request.POST.get('wo_id')
        civil_request = SiteData.objects.get(wo_id=searched_wo_id)
        civil_request.delete()
        delete_success = "Request deleted successfully"
        context.update({"delete": "yes"})
        return render(request, "civil_technical_office/civil_tech.html", context)

    elif request.method == 'POST' and 'export_data' in request.POST:
            print(request.POST)
            items=[]
            servant_items=[]
            ##searched by site_id
            if 'site_id' in request.POST:
                print("hello")
                if request.POST.get('site_id')!='':
                    print(request.POST.get('site_id'))
                    searched_site_id= request.POST.get('site_id')
                    site_items=SiteData.objects.filter(site_id=searched_site_id)
                    items=chain(site_items,items)
                    print(type(items))
                    site_servant_items = general_info.objects.filter(site_id=searched_site_id)
                    servant_items = chain(site_servant_items, servant_items)
                    # servant_items = False
                    # print(servant_items)

            ##searched by consultant name
            else:
            ##searched by consultant name
                if request.POST.get('consultant_name')!='':
                    searched_consultant_name= request.POST.get('consultant_name')
                    searched_consultant_items=SiteData.objects.filter(consultant_name=searched_consultant_name)
                    items = chain(searched_consultant_items, items)
                    servant_items = False

            ##searched by project name

                if request.POST.get('project_name')!='':
                    searched_project_name= request.POST.get('project_name')
                    searched_project_items=SiteData.objects.filter(project_name=searched_project_name)
                    items = chain(searched_project_items, items)
                    servant_items = False

            ##searched by project name

                if request.POST.get('region')!='':
                    searched_region= request.POST.get('region')
                    print(searched_region)
                    searched_region_items=SiteData.objects.filter(region=searched_region)
                    items = chain(searched_region_items, items)
                    servant_items = False

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition']='attachment; filename="requests.csv"'
            writer = csv.writer(response, delimiter=',')
            
            writer.writerow([ 'Site ID','Area', 'RT/GF', 'Structure Type', ' Height','Consultant Name','Requester dept', 'Request Date',
                'New Requirement', 'Last Visit Date', 'Status', ' Feedback', 'Requester',
                'Remarks', 'Mail Name', 'Project Name', 'Site Case', 'Building', 'Max Rating In',
                'Max Rating Per', 'Consultant Recommendations', 'Action Taken', 'Star Site', 
                'Employee ID', 'In Progress Date', 'Done Date', 'Work Order ID'])
        
            if servant_items:  
                for obj in items:
                    for obj2 in servant_items:
                        print(obj2.region)
                        writer.writerow([obj.site_id, obj2.region, obj2.site_type, obj2.structure_type, obj2.height, obj.consultant_name, obj.requester_dept, obj.request_date, 
                        obj.new_requirement, obj.last_visit, obj.status, obj.feedback, obj.requester, obj.remarks,
                        obj.mail_name, obj.project_name, obj.site_case, obj.building, obj.max_rating_in, 
                        obj.max_rating_per, obj.consultant_recommendations, obj.action_taken, obj.star_site, obj.employee_id,
                        obj.in_progress_date, obj.done_date , obj.wo_id])
            
            else:
                for obj in items:
                    print(obj.region)
                    writer.writerow([obj.site_id,obj.region, obj.site_type, obj.structure_type, obj.height, obj.consultant_name, obj.requester_dept, obj.request_date,
                        obj.new_requirement, obj.last_visit, obj.status, obj.feedback, obj.requester, obj.remarks,
                        obj.mail_name, obj.project_name, obj.site_case, obj.building, obj.max_rating_in, 
                        obj.max_rating_per, obj.consultant_recommendations, obj.action_taken, obj.star_site, obj.employee_id,
                        obj.in_progress_date, obj.done_date , obj.wo_id])
            return response

    else:
        return render(request, "civil_technical_office/civil_tech.html")
    