from rest_framework import serializers
from .models import Co2


class Co2Serializer(serializers.ModelSerializer):

    # redefine datetime in order to specify date format
    datetime = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Co2
        fields = ['datetime', 'co2_rate']  # '__all__' #

    def create(self, validated_data):
        return Co2(**validated_data)
