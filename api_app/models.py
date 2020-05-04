from django.db import models


class Co2(models.Model): 
    datetime = models.DateTimeField(blank=True, null=True)
    co2_rate = models.IntegerField(blank=True, null=True)  
    
    class Meta:
        app_label = 'api_app'
        db_table = 'co2'