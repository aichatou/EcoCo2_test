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

@api_view(['GET', 'POST'])
def co2_list(request):
    """
    List all code co2s, or create a new hat.
    """
    if request.method == 'GET':
        co2s = Co2.objects.all()
        serializer = Co2Serializer(co2s, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Co2Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		

@api_view(['GET', 'PUT', 'DELETE'])
def co2_detail(request, pk):  
    """
    Retrieve, update or delete a co2.
    """
    try:
        co2 = Co2.objects.get(id=pk)
    except Co2.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Co2Serializer(co2)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Co2Serializer(co2, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        co2.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def pandaPart(request): 
    #--------- interpolate data and save result in csv file -----------------
    data = Co2.objects.all().values('datetime', 'co2_rate') 
    data_df = pd.DataFrame(data) # convert data(d) to panda dataframe  
    data_df['datetime'] = pd.to_datetime(data_df['datetime'], utc=True) # convert data's datetime field to datetime format
    data_df2 = data_df.set_index('datetime')  # set datetime field as dataframe's index
    data_interpol = data_df2.resample('15T').mean().interpolate('linear')  # resample - mean - interpolate data to deal with missing values (nan)
    data_interpol.to_csv('data_interpol.csv', sep=';') # save data interpolated in csv format
	
	#----------- data difference --------------------------
    data_diff = data_df2.sub(data_interpol) # difference between data_df2 and data_interpol 
    # plot data_diff and save it in png file 
    plt.figure() 
    data_diff.plot()
    plt.savefig("co2data.png")   

	#--------- median of each season -----------------------
    # with initial data: data_df2
    Winter = data_df2[data_df2.index.month.isin([12,1,2,3])].median()
    Spring = data_df2[data_df2.index.month.isin([4,5])].median()
    Summer = data_df2[data_df2.index.month.isin([6,7,8,9])].median()
    Fall = data_df2[data_df2.index.month.isin([10,11])].median()
    # with interpolated dara: data_interpol
    Winter_interpol = data_interpol[data_interpol.index.month.isin([12,1,2,3])].median()
    Spring_interpol = data_interpol[data_interpol.index.month.isin([4,5])].median()
    Summer_interpol = data_interpol[data_interpol.index.month.isin([6,7,8,9])].median()
    Fall_interpol = data_interpol[data_interpol.index.month.isin([10,11])].median()

    # ---------------- mean of weekend / weekday ------------
    # with initial data: data_df2
    Weekday_data = data_df2[data_df2.index.weekday.isin([0,1,2,3,4])].mean() #52.093406
    Weekend_data = data_df2[data_df2.index.weekday.isin([5,6])].mean()
    # with interpolated dara: data_interpol
    Weekday_interpol = data_interpol[data_interpol.index.weekday.isin([0,1,2,3,4])].mean()
    Weekend_interpol = data_interpol[data_interpol.index.weekday.isin([5,6])].mean()

