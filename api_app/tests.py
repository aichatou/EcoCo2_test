from rest_framework import status
from django.urls import reverse  
from rest_framework.test import APITestCase
from .views import Co2Serializer
import json
from api_app.models import Co2


class Co2Api(APITestCase):

    def setUp(self):

        self.valid_co2 = {
            'datetime': '2017-01-01T01:30:00',
            'co2_rate': 33
        }   
        
        self.invalid_co2 = {
            'datetime': '2017-01-01T01:30:00',
            'co2_rate': 33.74
        }


        self.detail_url = reverse('co2Detail', kwargs={'pk': 15}) 
        self.list_url = reverse('co2List')

