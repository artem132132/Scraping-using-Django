from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
from .models import Hotel_info
from .city_list import city_list
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import HotelInfoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

# Create your views here.
def get_soup_data(url: str, city_name: str) -> BeautifulSoup:
    driver = Chrome()
    driver.get(url)
    driver.implicitly_wait(1.5)

    driver.find_element(By.ID, "hotels-destinationV8").send_keys(city_name)
    time.sleep(2.0)

    search_button = driver.find_element(By.CLASS_NAME, "search-btn-wrap")
    search_button.click()
    time.sleep(4.0)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup


def get_hotel_data(city_name: str) -> list:
    url="https://us.trip.com/hotels/?locale=en-US&curr=USD"

    soup = get_soup_data(url = url, city_name = city_name)
    all_data = soup.find("ul", class_="long-list long-list-v8")

    all_hotel_data_of_a_city = []

    for each_hotel in all_data.find_all("div", class_="compressmeta-hotel-wrap-v8"):
        hotel_name = each_hotel.find("span", class_="name")
        hotel_rating = each_hotel.find("span", class_="real")
        hotel_review = each_hotel.find("div", class_="count")
        room_description = each_hotel.find("span", class_="room-panel-roominfo-name")
        location = each_hotel.find("p", class_="transport")
        room_policy = each_hotel.find("div", class_="room-policy")
        price_incl_tax = each_hotel.find("span", class_="not-break")
        hotel_id = each_hotel['id']
        hotel_url = f"https://us.trip.com/hotels/detail/?hotelId={hotel_id}"

        if hotel_name == None or hotel_rating == None or hotel_review == None or room_description == None or location == None or room_policy == None or price_incl_tax == None:
            continue
        else:
            hotel_name = hotel_name.get_text()
            hotel_rating = hotel_rating.get_text()
            hotel_review = hotel_review.get_text()
            room_description = room_description.get_text()
            location = location.get_text()
            location = location.replace('Show on Map', '')
            room_policy = room_policy.get_text()
            price_incl_tax = price_incl_tax.get_text()

        all_hotel_data_of_a_city.append([hotel_id, hotel_name, hotel_rating, hotel_review, room_description, location, city_name, room_policy, price_incl_tax, hotel_url] )

    return all_hotel_data_of_a_city


def save_hotel_info_in_db(city_name: str) -> None:
        all_hotel_info = get_hotel_data(city_name=city_name)
        all_data_list = [Hotel_info(hotel_id = each_hotel_info[0], hotel_name = each_hotel_info[1], rating = each_hotel_info[2], hotel_review = each_hotel_info[3],
                            room_description = each_hotel_info[4], location = each_hotel_info[5],
                            city_and_country = each_hotel_info[6], room_policy = each_hotel_info[7], price_incl_tax = each_hotel_info[8], hotel_url = each_hotel_info[9])
                 for each_hotel_info in all_hotel_info]

        Hotel_info.objects.bulk_create(all_data_list)


def insert_hotel_data(request) -> HttpResponse:
    for each_city in city_list:
        try:
            save_hotel_info_in_db(each_city)
        except:
            return HttpResponse("Error!")

    return HttpResponse("Saved!")


# View for showing data by paginator using django ORM
def show_all_data(request) -> Response:
    all_data = Hotel_info.objects.all()
    paginator_data = Paginator(all_data, 30)
    page_number = request.GET.get('page')
    try:
        hotels = paginator_data.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        hotels = paginator_data.page(1)
    except EmptyPage:
        # if page is empty then return last page
        hotels = paginator_data.page(paginator_data.num_pages)
    context = {'hotels': hotels}
    # sending the page object to index.html
    return render(request, 'show_hotel_data.html', context)


# Implementation of Django Rest Framework (DRF)
@api_view(['GET'])
def show_all_by_drf(request) -> Response:
    result = Hotel_info.objects.all()
    serializers = HotelInfoSerializer(result, many=True)
    return Response(serializers.data)


# DRF Pagination
@api_view(['GET'])
def show_all_drf_by_page(request) -> Response:
    paginator = PageNumberPagination()
    paginator.page_size = 25
    result = Hotel_info.objects.all()
    result_page = paginator.paginate_queryset(result, request)
    serializers = HotelInfoSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializers.data)


@api_view(['POST'])
def post_data_by_drf(request) -> Response:
    serializer = HotelInfoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def hotel_details(request, id : int) -> Response:
    try:
        hotel_data = Hotel_info.objects.get(id=id)
    except Hotel_info.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializers = HotelInfoSerializer(hotel_data)
        return Response(serializers.data)

    elif request.method == 'PUT':
        serializer = HotelInfoSerializer(hotel_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        hotel_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        serializer = HotelInfoSerializer(hotel_data, data=request.data, partial=True)  # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)






# View for showing data using DRF serializer
# @api_view(['GET', 'POST'])
# def show_all_by_drf_get(request) -> Response:
#
#     if request.method == 'GET':
#         result = Hotel_info.objects.all()
#         serializers = HotelInfoSerializer(result, many=True)
#         return Response(serializers.data)
#
#     elif request.method == 'POST':
#         # data = JSONParser().parse(request)
#         # serializer = HotelInfoSerializer(data=data)
#         # print(request.data)
#         # if serializer.is_valid():
#         #     serializer.save()
#         #     return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         hotel_id = request.data['hotel_id']
#         hotel_name = request.data['hotel_name']
#         rating = request.data['rating']
#         hotel_review = request.data['hotel_review']
#         room_description = request.data['room_description']
#         location = request.data['location']
#         city_and_country = request.data['city_and_country']
#         room_policy = request.data['room_policy']
#         price_incl_tax = request.data['price_incl_tax']
#         hotel_url = request.data['hotel_url']
#
#         print(hotel_id, hotel_name , rating , hotel_review , room_description ,
#                                 location , city_and_country , room_policy , price_incl_tax , hotel_url )
#
#         hotel_data = Hotel_info(hotel_id = hotel_id, hotel_name = hotel_name, rating = rating, hotel_review = hotel_review, room_description = room_description,
#                                 location = location, city_and_country = city_and_country, room_policy = room_policy, price_incl_tax = price_incl_tax, hotel_url = hotel_url)
#
#         try:
#             hotel_data.save()
#             return HttpResponse("New data is saved!")
#         except:
#             return HttpResponse("Error! Cannot save")









# '{"hotel_id":100,"hotel_name":"shdf","rating":"This field is required.","hotel_review":"This field is required.","room_description":"This field is required.","location":"This field is required.","city_and_country":"This field is required.","room_policy":"This field is required.","price_incl_tax":"This field is required.","hotel_url":"This field is required."}'