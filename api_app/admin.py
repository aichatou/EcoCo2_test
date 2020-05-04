from django.contrib import admin
from .models import Co2


class Co2Admin(admin.ModelAdmin):
    list_display = ('datetime', 'co2_rate')


admin.site.register(Co2, Co2Admin)
