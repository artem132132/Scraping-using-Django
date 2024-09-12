from rest_framework import serializers
from .models import Hotel_info


# class HotelInfoSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     hotel_id = serializers.IntegerField()
#     hotel_name = serializers.CharField()
#     rating = serializers.CharField()
#     hotel_review = serializers.CharField()
#     room_description = serializers.CharField()
#     location = serializers.CharField()
#     city_and_country = serializers.CharField()
#     room_policy = serializers.CharField()
#     price_incl_tax = serializers.CharField()
#     hotel_url = serializers.CharField()


# This serializer class can be defined as below:
class HotelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel_info
        fields = ('__all__')