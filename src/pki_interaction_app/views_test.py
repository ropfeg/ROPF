import xlwt
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import pki_record, pki_source
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from pandas import read_excel,Timestamp,concat


# Create your views here.


def export_requested(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="PKI_Batch.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('PKI_Records')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Site_ID', 'Vendor', 'Serial', 'Activity', 'Region', 'Function', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = pki_record.objects.filter(pki_status1="Requested").values_list('site_id', 'vendor', 'serial', 'activity',
                                                                          'region', 'function', )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    print(datetime.date.today())
    # update batch after export with status Request in-progress
    pki_record.objects.filter(pki_status1="Requested").update(admin_export_date=datetime.date.today())
    pki_record.objects.filter(pki_status1="Requested").update(pki_status1='Request in-progress')

    return response


def export_all(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="../static/Sample_Template/PKI_Batch.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('PKI_Records')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['id','Site_ID', 'Vendor', 'Serial', 'Activity', 'Region', 'Function',
               'pki_status_1','pki_status_2','CRQ_status','CRQNo._Add','Batch#',
               'username','CollectionDate','adminExportDate','CRQcreationDate',
               'CRQExecutionDate','export_collect','create_export','execute_create','Total issue lifetime','SLA Comment','Request Type']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = pki_record.objects.all().values_list( )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)

    return response

def source_export_all(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="../static/Sample_Template/PKI_Batch.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('PKI_Records')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['id','serials','vendor' ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = pki_source.objects.all().values_list()
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)

    return response

# # import from user

# # PKI SOURCE

def pki_upload(request):
    context = {"ss_result": "", "sa_result": "", "ba_result": "", "result_xls": "", "ss_js": "", "ba_js": "",
               "sa_js": "", "admin": ""}

    # batch add
    if request.method == 'POST' and ("batch_add" in request.POST):
        myfile = request.FILES['myfile']

        df = read_excel(myfile)
        df["Status"] = ""

        try:

            for ind in df.index:
                s = df["Serial"][ind]
                if pki_source.objects.filter(serials=s).exists():
                    df["Status"][ind] = "Exist"

                elif pki_record.objects.filter(serial=s).exclude(pki_status2 ="Removed").exists():
                    record = pki_record.objects.filter(serial=s).exclude(pki_status2="Removed").values("pki_status1")
                    df["Status"][ind] =record[0]["pki_status1"]

                else:
                    pki_record.objects.create(
                        site_id=df["SiteID"][ind],
                        vendor=df["Vendor"][ind],
                        serial=df["Serial"][ind],
                        activity=df["Activity"][ind],
                        region=df["Region"][ind],
                        function=df["Function"][ind],
                        req_type=df["Request Type"][ind],
                        pki_status1="Requested",
                        collection_date=datetime.date.today(),
                        crq_status="Need CRQ",
                    )

                    df["Status"][ind] = "requested"

                df.to_excel("./static/Sample_Template/result.xlsx")

            context = {"ba_result": "Your file uploaded successfully and being processed, thank you.",
                       "result_xls": "../static/Sample_Template/result.xlsx", "ba_js": "correct"}

        except (KeyError) as e:
            context = {"ba_js": "incorrect"}
        return render(request, 'pki/pki.html', context)




    # # single add
    elif request.method == 'POST' and ("single_add" in request.POST):
        site_id = request.POST.get("site_id")
        vendor = request.POST.get("vendor")
        serial = request.POST.get("serial")
        activity = request.POST.get("activity")
        function = request.POST.get("function")
        region = request.POST.get("region")
        request_type=request.POST.get("request_type")
        f = request.POST.items()
        print(region)
        print(request_type)

        if pki_source.objects.filter(serials=serial).exists():

            context = {"sa_result": "The serial No. status is Exists in PKI Server.", "sa_js": "Exist"}



        elif pki_record.objects.filter(serial=serial).exclude(pki_status2="Removed").exists():

            record = pki_record.objects.filter(serial=serial).exclude(pki_status2="Removed").values("pki_status1")
            context = {"sa_result": record[0]["pki_status1"], "sa_js": "Exist"}

        else:

            pki_record.objects.create(
                site_id=site_id,
                vendor=vendor,
                serial=serial,
                activity=activity,
                region=region,
                function=function,
                req_type=request_type,
                pki_status1="Requested",
                collection_date=datetime.date.today(),
                crq_status="Need CRQ",
            )

            context = {
                "sa_result": "Your Request is being processed, an e-mail requesting CRQ will be sent soon, thank you.",
                "sa_js": "submit"}
        return render(request, 'pki/pki.html', context)




    # # single search
    elif request.method == 'POST' and ("single_search" in request.POST):
        ss = request.POST.get("single_serial")

        if pki_source.objects.filter(serials=ss).exists():

            context = {"ss_result": "Exists", "ss_js": "exist"}
            return render(request, 'pki/pki.html', context)
        elif pki_record.objects.filter(serial=ss).exclude(pki_status2="Removed").exists():
            record = pki_record.objects.filter(serial=ss).exclude(pki_status2="Removed").values("pki_status1")

            context = {"ss_result": record[0]["pki_status1"], "ss_js": "exist"}

        else:
            context = {"ss_result": "The serial No. NOT Exists in PKI Server.", "ss_js": "not_exist"}



    elif request.method == 'POST' and ("export_requests" in request.POST):
        export_requested(request)



        # admin update function
    # elif request.method == 'POST' and ("admin_batch_add" in request.POST):
    #     myfile = request.FILES['myfile']
    #     print("start")
    #     df = read_excel(myfile)

    #     for ind in df.index:

    #         pki_record.objects.create(
    #                     site_id             =df["SiteID"][ind],
    #                     vendor              =df["Vendor"][ind],
    #                     serial              =df["Serial"][ind],
    #                     activity            =df["Activity"][ind],
    #                     region              =df["Region"][ind],
    #                     function            =df["Function"][ind],
    #                     pki_status1         =df["pki_status_1"][ind],
    #                     pki_status2         =df["pki_status_2"][ind],
    #                     crq_status          =df["CRQ_status"][ind],
    #                     crq_no              =df["CRQNo._Add"][ind],
    #                     batch_no            =df["Batch#"][ind],
    #                     req_type            =df["Request Type"][ind],
    #                     username            =df["username"][ind],
    #                     collection_date     =df["CollectionDate"][ind],
    #                     admin_export_date   =df["adminExportDate"][ind],
    #                     crq_creation_date   =df["CRQcreationDate"][ind],
    #                     crq_executation_date=df["CRQExecutionDate"][ind],
    #                     pki_comment         =df["SLA Comment"][ind],


    #                 )
    #         context = {"ba_result": "Your file uploaded successfully and being processed, thank you.",
    #                    "result_xls": "../static/Sample_Template/result.xlsx", "ba_js": "correct"}





    # elif request.method == 'POST' and ("src_update" in request.POST):
    #     myfile = request.FILES['myfile']
    #     df_upload = read_excel(myfile)
    #     df_src=read_excel("./static/Sample_Template/src_db.xlsx")
    #     print("start")
    #     print(df_upload)
    #     print(df_src)
    #     remove_check = df_upload["Serials"].values.tolist()
    #     remove=df_src[~df_src.Serials.isin(remove_check)]
    #     remove.to_excel("remove.xlsx")
    #     add_check=df_src["Serials"].values.tolist()
    #     add = df_upload[~df_upload.Serials.isin(add_check)]

    #     add.to_excel("add.xlsx")

    #     for ind in remove.index:
    #         print("remove")
    #         pki_source.objects.filter(serials=remove["Serials"][ind]).delete()
    #         if pki_record.objects.filter(serial=remove["Serials"][ind]).exclude(pki_status2="Removed").exists():
    #             pki_record.objects.filter(serial=remove["Serials"][ind]).update( pki_status2='Removed')
    #     for ind in add.index:
    #         print("add")
    #         pki_source.objects.create(
    #                     serials=add["Serials"][ind],
    #                     vendor=add["Vendor"][ind],

    #                 )
    #         if pki_record.objects.filter(serial=add["Serials"][ind]).exclude(pki_status2="Removed").exists():
    #             pki_record.objects.filter(serial=add["Serials"][ind]).update( pki_status1='Exist',
    #                                                                           crq_status="Done",
    #                                                                           crq_executation_date=datetime.date.today(),

    #                                                                           )
    #     df_upload.to_excel("./static/Sample_Template/src_db.xlsx")
    #     context={"admin_result": "correct"}
    #     return render(request, 'pki/pki.html', context)
    # elif request.method == 'POST' and ("crq_update" in request.POST):
    #     myfile = request.FILES['crqfile']
    #     df_upload = read_excel(myfile)
    #     print(df_upload)
    #     for ind in df_upload.index:
    #         pki_record.objects.filter(serial=df_upload["SerialNo."][ind]).update(
    #                                                                         crq_no=df_upload["CRQNumber"][ind],
    #                                                                         crq_status="RFA",
    #                                                                         crq_creation_date=datetime.date.today())
    #         print("crq_add")
    #     context = {"admin_result": "correct"}


    return render(request, 'pki/pki.html', context)



