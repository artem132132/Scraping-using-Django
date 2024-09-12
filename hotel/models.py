from django.db import models

# Create your models here.
class Hotel_info(models.Model):
    hotel_id = models.BigIntegerField(unique=True)
    hotel_name = models.CharField(max_length=250, null=False)
    rating = models.CharField(max_length=250, null=False)
    hotel_review = models.CharField(max_length=250)
    room_description = models.CharField(max_length=250)
    location = models.CharField(max_length=250, null=False)
    city_and_country = models.CharField(max_length=250, null=False)
    room_policy = models.CharField(max_length=250)
    price_incl_tax = models.CharField(max_length=250, null=False)
    hotel_url = models.TextField(unique=True, null=False)

