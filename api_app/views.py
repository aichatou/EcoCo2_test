from .models import Co2
from .serializers import Co2Serializer
import datetime
import pandas as pd
import requests
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
import matplotlib.pyplot as plt


# ---------------------------------- django block --------------------------------------------------------------------------
# get 2017 and 2018 data from api
def get_data(request):  # used only once to get and save data in sqlite database
    start = int((datetime.datetime(2017, 1, 1) - datetime.datetime(1970, 1, 1)
                 ).total_seconds())  # start date (2017/01/01)
    end = int((datetime.datetime(2018, 12, 31) - datetime.datetime(1970, 1, 1)).total_seconds())  # end date (2018/12/31)
    url = "https://api-recrutement.ecoco2.com/v1/data/?start="+str(start)+"&end="+str(end)  # api endpoint to get data
    r = requests.get(url)  # api data
    datas = r.json()  # convert api data to json format
    for item in datas:
        serializer = Co2Serializer(data=item)
        if not serializer.is_valid():  # check data validation
            return HttpResponse("<h1> Data load: Fail</h1>")  # print error message
        obj = Co2()  # create empty Co2 data_object
        obj.datetime = item['datetime']  # add datetime value to obj
        obj.co2_rate = item['co2_rate']  # add co2_rate value to obj 
        existObjs = Co2.objects.filter(datetime = obj.datetime, co2_rate=obj.co2_rate)
        if len(list(existObjs)) > 0:
             pass
        else:
             obj.save()
        obj.save()  # save obj in database
    return render(request, 'load_data_message.html')  # print a success message


@api_view(['GET', 'POST'])
def co2_list(request):
    """
    List all code co2s, or create a new co2.
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
    # --------- interpolate data and save result in csv file -----------------
    data = Co2.objects.all().values('datetime', 'co2_rate')
    data_df = pd.DataFrame(data)  # convert data(d) to panda dataframe
    # convert data's datetime field to datetime format
    data_df['datetime'] = pd.to_datetime(data_df['datetime'], utc=True)
    data_df2 = data_df.set_index('datetime')  # set datetime field as dataframe's index
    # resample - mean - interpolate data to deal with missing values (nan)
    data_interpol = data_df2.resample('15T').mean().interpolate('linear')
    data_interpol.to_csv('results/data_interpol.csv', sep=';')  # save data interpolated in csv format

    # ----------- data difference --------------------------
    data_diff = data_df2.sub(data_interpol)  # difference between data_df2 and data_interpol
    # plot data_diff and save it in png file
    plt.figure()
    data_diff.plot()
    plt.savefig("co2data.png")

    # --------- median of each season -----------------------
    # with initial data: data_df2
    Winter = data_df2[data_df2.index.month.isin([12, 1, 2, 3])].median()
    Spring = data_df2[data_df2.index.month.isin([4, 5])].median()
    Summer = data_df2[data_df2.index.month.isin([6, 7, 8, 9])].median()
    Fall = data_df2[data_df2.index.month.isin([10, 11])].median()
    # with interpolated dara: data_interpol
    Winter_interpol = data_interpol[data_interpol.index.month.isin([12, 1, 2, 3])].median()
    Spring_interpol = data_interpol[data_interpol.index.month.isin([4, 5])].median()
    Summer_interpol = data_interpol[data_interpol.index.month.isin([6, 7, 8, 9])].median()
    Fall_interpol = data_interpol[data_interpol.index.month.isin([10, 11])].median()

    # ---------------- mean of weekend / weekday ------------
    # with initial data: data_df2
    Weekday_data = data_df2[data_df2.index.weekday.isin([0, 1, 2, 3, 4])].mean()  # 52.093406
    Weekend_data = data_df2[data_df2.index.weekday.isin([5, 6])].mean()
    # with interpolated dara: data_interpol
    Weekday_interpol = data_interpol[data_interpol.index.weekday.isin([0, 1, 2, 3, 4])].mean()
    Weekend_interpol = data_interpol[data_interpol.index.weekday.isin([5, 6])].mean()

    # -------------- csv file ------------------------------------------------------------------------------
    # get csv data
    csvData = pd.read_csv('eco2mix-national-cons-def.csv', sep=';')  # read data from csv file
    datetime = list(csvData['Date et Heure'])  # get date field from csvData and convert to list format
    co2 = list(csvData['Taux de CO2 (g/kWh)'])  # read co2 field from csvData and convert to list format
    d = {'datetime': datetime, 'co2': co2}  # put datetime and co2 in a dictionnary
    # interpolate data and save result in csv file
    csv_data_df = pd.DataFrame(d)
    csv_data_df['datetime'] = pd.to_datetime(data_df['datetime'], utc=True)
    csv_data_df2 = data_df.set_index('datetime')
    csv_data_interpol = csv_data_df2.resample('15T').mean().interpolate('linear')
    csv_data_interpol.to_csv('results/csv_data_interpol.csv', sep=';')
    # calculate co2 production
    co2Prod = csv_data_interpol.sum()

    co2Produc = list(co2Prod)[0]
    mean_week = [list(Weekday_data)[0], list(Weekend_data)[0]]
    interpolated_week = [list(Weekday_interpol)[0], list(Weekend_interpol)[0]]
    median_season = [list(Winter)[0], list(Spring)[0], list(Summer)[0], list(Fall)[0]]
    interpolated_median_season = [list(Winter_interpol)[0], list(Spring_interpol)[0],
                                  list(Summer_interpol)[0], list(Fall_interpol)[0]]

    resulting_data = {'co2Produc': co2Produc, 'mean_week': mean_week, 'interpolated_week': interpolated_week, 'median_season': median_season,
                      'interpolated_median_season': interpolated_median_season}

    return render(request, 'panda_result.html', resulting_data)
