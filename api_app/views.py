from .models import Co2
from rest_framework import serializers
from rest_framework import viewsets
import datetime
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd
from django.conf import settings
import requests
from .models import Co2
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest, HttpResponse  
from rest_framework.decorators import api_view
import matplotlib.pyplot as plt


# ---------------------------------- django block --------------------------------------------------------------------------
# get 2017 and 2018 data from api  
def get_data(request):  # used only once to get and save data in postgresql database
    start = int((datetime.datetime(2017,1,1) - datetime.datetime(1970,1,1)).total_seconds()) # start date (2017/01/01)
    end = int((datetime.datetime(2018,12,31) - datetime.datetime(1970,1,1)).total_seconds()) # end date (2018/12/31)
    url = "https://api-recrutement.ecoco2.com/v1/data/?start="+str(start)+"&end="+str(end) # api endpoint to get data
    r = requests.get(url) # api data
    datas = r.json() # convert api data to json format
    for item in datas:  
      serializer = Co2Serializer(data=item)
      if not serializer.is_valid(): # check data validation
          return HttpResponse("<h1> Data load: Fail</h1>") # print error message 
      obj = Co2() # create empty Co2 data_object
      obj.datetime = item['datetime'] # add datetime value to obj
      obj.co2_rate= item['co2_rate'] # add co2_rate value to obj
      obj.save() # save obj in database
    return HttpResponse("<h1> Data load: Success</h1>")  # print a success message  
    
      
# ------------------- Co2 serializer class ----------------------------------------------------------------------------
class Co2Serializer(serializers.ModelSerializer): 

    datetime = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S") # redefine datetime in order to specify date format
    class Meta:
        model = Co2
        fields = ['datetime', 'co2_rate']  #'__all__' #

    def create(self, validated_data):
        return Co2(**validated_data)   
