from __future__ import unicode_literals
import io
import csv
import json
import codecs
import time
from django.http import JsonResponse, HttpResponse
from tqdm import tqdm
from django.shortcuts import render
from django.conf import settings
from .database import dbs as db
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
flag = []
def home(request):
    return render(request,'upload.html')

def check_new_entry(request):
    if request.method == 'POST':
        try:
            files = request.FILES['datafile']
            with open(str(files),"r",) as fl:
                spamreader = csv.reader(codecs.iterdecode(files, 'utf-8'))
                row_count = sum(1 for row in fl )
            count = 0
            data = []
            head_list = []
            global flag
            flag = False
            print('Processing the Upload')
            iterator = tqdm(spamreader,total=row_count)
            for row in iterator:
                time.sleep(0.1)
                if(flag == True):
                    break
                if ( count == 0 ):
                    head_list = row
                    count = count + 1
                else: 
                    data.append(dict(zip(head_list, row)))
                    count= count +1
            print("Complete/Finish")
            if(flag == False):
                db.test.insert(data)
            return JsonResponse( {'code': '1',
                            'Message':'Succesfully added data to database',
                            'status': 'success'})
        except Exception as e:
            print(type(e))

def stop_csv(request):
    global flag
    flag = True
    return render(request,'upload.html')
    # return JsonResponse( {'code': '0',
	# 						'Message':'Fail to process/Force stopped',
	# 						'status': 'fail'})

def export_details(request):
    return render(request,'export_detail.html')

def get_csv_export(request):
    if request.method == 'POST':
        field_type = request.POST.get('type')
        field_value = request.POST.get('value')
    elif request.method == 'GET':
        field_type = request.GET.get('type')
        field_value = request.GET.get('value')
    dbt = db.test
    buffer = io.StringIO()
    wr = csv.writer(buffer, quoting=csv.QUOTE_ALL)
    results = dbt.find({}).limit(1)
    for head in results:
        head_list = [*head]
        break
    wr.writerow(head_list)
    if(field_type == '' and field_value == '' ):
        count = dbt.count()
    else:
        count = dbt.count({field_type:field_value})
    limit = 10
    global flag
    flag = False
    print('Processing the CSV Export in the chuncks of 10 values each time.')
    for j in tqdm(range(0,int(count/limit)+1),total=int(count/limit)):
        if(flag == True):
            break
        if(field_type == '' and field_value == '' ):
            res = dbt.find({}).limit(limit).skip(limit*j)
        else:
            res = dbt.find({field_type : field_value}).limit(limit).skip(limit*j)
        for value in res:
            wr.writerow(value.values())
    print('Complete/Finish!')
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=csv_export.csv'
    return response



    


