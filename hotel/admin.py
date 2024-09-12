from django.contrib import admin
from .models import Hotel_info

# Register your models here.

class Hotel_info_admin(admin.ModelAdmin):
    list_display = ("id", "hotel_name", "price_incl_tax", "location", "city_and_country", "hotel_url")

admin.site.register(Hotel_info, Hotel_info_admin)