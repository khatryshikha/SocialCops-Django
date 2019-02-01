from __future__ import unicode_literals
import os
import csv
import codecs
import time
from django.http import JsonResponse
from tqdm import tqdm
from django.shortcuts import render
from django.conf import settings
from .database import dbs as db

# Create your views here.
flag = False
def home(request):
    return render(request,'upload.html')

def check_new_entry(request):
    if request.method == 'POST':
        files = request.FILES['datafile']
        with open(str(files),"r",) as fl:
            spamreader = csv.reader(codecs.iterdecode(files, 'utf-8'))
            row_count = sum(1 for row in fl )
        count = 0
        data = []
        head_list = []
        global flag
        flag = False
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
        if(flag == False):
            db.test.insert(data)
        return JsonResponse( {'code': '1',
						'Message':'Succesfully added data to database',
						'status': 'success'})

def stop_csv(request):
    global flag
    flag = True
    return JsonResponse( {'code': '0',
							'Message':'Fail to process/Force stopped',
							'status': 'fail'})