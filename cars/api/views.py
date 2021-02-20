from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from cars.models import Car, Rate 
from .serializers import CarCreateSerializer, CarSerializer, CarPopularSerializer, RateSerializer

@api_view(['GET', 'POST'])
def get_post_cars(request):
    # get all cars
    if request.method == 'GET':
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)
    # insert a new record for a car
    elif request.method == 'POST':  
        data = {
            'make': request.data.get('make'),
            'model': request.data.get('model')
        }
        if len(data['make']) > 0:
            address = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{data['make']}?format=json"
            response_raw = requests.get(address)
            response = response_raw.json()
            for car in response['Results']:
                if data['model'].casefold() == car['Model_Name'].casefold() and data['make'].casefold() == car['Make_Name'].casefold():
                    serializer = CarCreateSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("This car (make & model) does not exist", status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_car(request, pk):
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    car.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def post_rate(request):
    data = {
        'car_id': request.data.get('car_id'),
        'rating': request.data.get('rating')
    }
    serializer = RateSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        car = Car.objects.get(pk=data['car_id'])
        car.avg_rating = (car.avg_rating*car.rates_number+int(data['rating']))/(car.rates_number+1)
        car.rates_number += 1
        car.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_popular_cars(request):
    cars = Car.objects.all().order_by('-rates_number')[:10]
    serializer = CarPopularSerializer(cars, many=True)
    return Response(serializer.data)   
