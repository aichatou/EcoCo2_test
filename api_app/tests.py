from rest_framework import status
from django.urls import reverse  
from rest_framework.test import APITestCase
from .views import Co2Serializer
import json
from api_app.models import Co2


class Co2Api(APITestCase):

