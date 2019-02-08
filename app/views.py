from __future__ import unicode_literals
import io
import csv
import json
import codecs
import time
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from tqdm import tqdm
from django.shortcuts import render
from django.conf import settings
from .database import dbs as db
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
flag = []
@csrf_exempt
def home(request):
    db.test.remove({})
    return render(request,'upload.html')

@csrf_exempt
def check_new_entry(request):
    if request.method == 'POST':
        files = request.FILES['datafile']
    try:   
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
        return HttpResponse(e)

@csrf_exempt
def stop_csv(request):
    global flag
    flag = True
    if request.method == 'POST':
         return JsonResponse( {'code': '0',
							'Message':'Fail to process/Force stopped',
							'status': 'fail'})
    else:
        return JsonResponse( {'code': '0',
							'Message':'Fail to process/Force stopped',
							'status': 'fail'})
@csrf_exempt
def export_details(request):
    return render(request,'export_detail.html')

@csrf_exempt
def get_csv_export(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        price = request.POST.get('price')
    elif request.method == 'GET':
        name = request.GET.get('name')
        startdate = request.GET.get('startdate')
        enddate = request.GET.get('enddate')
        price = request.GET.get('price')
    try:
        if(name == ""): name=None
        if(price == ""): price=None
        if(startdate == ""): startdate=None
        if(enddate == ""): enddate=None
    
        dbt = db.test
        count = 0
        buffer = io.StringIO()
        wr = csv.writer(buffer, quoting=csv.QUOTE_ALL)
        results = dbt.find({}).limit(1)
        for head in results:
            head_list = [*head]
            break
        wr.writerow(head_list)
        if(name is None and (startdate is None and enddate is None) and price is None):
            count = dbt.count()
        else:
            if(name is not None):
                count = count + dbt.count({'country' : str(name)})
            if(price is not None):
                filters = price[0]+price[1]+price[2]
                price1 = price[4:]
                if(filters == 'gte'):
                    count = count + dbt.count({'price':{'$gte':price1}})
                elif(filters == 'lte'):
                    count = count + dbt.count({'price':{'$lte':price1}})
                elif(filters == 'eqt'):
                    count = count + dbt.count({'price':{'$eq':price1}})
            if(startdate is not None and enddate is not None):
                startdate1 = datetime.strptime(startdate, "%Y-%m-%d")
                enddate1 = datetime.strptime(enddate, "%Y-%m-%d")
                enddate1 = enddate1.replace(minute=59, hour=23, second=59)
                count = count + dbt.count({'date':{'$gte':str(startdate1),'$lte':str(enddate1)}})
            elif(startdate is not None):
                startdate1 = datetime.strptime(startdate, "%Y-%m-%d")
                count = count + dbt.count({'date':{'$gte':str(startdate1)}})
            elif(enddate is not None):
                enddate1 = datetime.strptime(enddate, "%Y-%m-%d")
                enddate1 = enddate.replace(minute=59, hour=23, second=59)
                count = count + dbt.count({'date':{'$lte':str(enddate1)}})
        limit = 5
        a=b=c=[]
        res = []
        global flag
        flag = False
        print('Processing the CSV Export in the chuncks of 10 values each time.')
        for j in tqdm(range(0,int(count/limit)+1),total=int(count/limit)):
            if(flag == True):
                break
            if(name is None and startdate is None and enddate is None and price is None):
                res = dbt.find({}).limit(limit).skip(limit*j)
            else:
                if(name is not None):
                    res1 = dbt.find({'country' : str(name)}).limit(limit).skip(limit*j)
                    a = [item for item in res1] 

                if(price is not None):
                    filters = price[0]+price[1]+price[2]
                    price1 = price[4:]
                    if(filters == 'gte'):
                        res2 = dbt.find({'price':{'$gte':price1}}).limit(limit).skip(limit*j)
                    elif(filters == 'lte'):
                        res2 = dbt.find({'price':{'$lte': price1}}).limit(limit).skip(limit*j)
                    elif(filters == 'eqt'):
                        res2 = dbt.find({'price':{'$eq': price1}}).limit(limit).skip(limit*j)
                    b = [item for item in res2] 
                if(startdate is not None and enddate is not None):
                    startdate1 = datetime.strptime(startdate, "%Y-%m-%d")
                    enddate1 = datetime.strptime(enddate, "%Y-%m-%d")
                    enddate1 = enddate1.replace(minute=59, hour=23, second=59)
                    res3 = dbt.find({'date':{'$gte':str(startdate1),'$lte':str(enddate1)}}).limit(limit).skip(limit*j)
                    c = [item for item in res3]   

                elif(startdate is not None):
                    startdate1 = datetime.strptime(startdate, "%Y-%m-%d")
                    res3 = dbt.find({'date':{'$gte':str(startdate1)}}).limit(limit).skip(limit*j)
                    c = [item for item in res3]   

                elif(enddate is not None):
                    enddate1 = datetime.strptime(enddate, "%Y-%m-%d")
                    enddate1 = enddate.replace(minute=59, hour=23, second=59)
                    res3 = dbt.find({'date':{'$lte':str(enddate1)}}).limit(limit).skip(limit*j) 
                    c = [item for item in res3]   

                res = a+b+c
            for value in res:
                wr.writerow(value.values())

        print('Complete/Finish!')
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=csv_export.csv'
        return response
    except Exception as e:
            return HttpResponse(e)


@csrf_exempt
def clear_db(request):
    db.test.remove({})
    return render(request,'upload.html')
    


