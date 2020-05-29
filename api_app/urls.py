from .views import get_data, co2_list, co2_detail, pandaPart
from django.urls import path


urlpatterns = [
    path('co2List/', co2_list, name='co2List'),  # path to get all co2 datas (/api_app/co2List)
    path('panda/', pandaPart, name='panda'),  # path to get results for pandaPart view function (/api_app/panda)

    # path('co2Detail/<int:pk>/', co2_detail, name='co2Detail'),  # path to get a single data object (/api_app/co2detail)
    # path('datas/', get_data, name='get_data'),  # path to load api data in database;
]
