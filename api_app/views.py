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

