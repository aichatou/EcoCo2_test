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

    def test_gel_all_data(self):

        response = self.client.get(self.list_url)
        co2s = Co2.objects.all()
        serializer = Co2Serializer(co2s, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_co2(self):
        response = self.client.post(
            self.list_url,
            data=json.dumps(self.valid_co2),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_co2(self):
        response = self.client.post(
            self.list_url,
            data=json.dumps(self.invalid_co2),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
