import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from cars.models import Car, Rate
from cars.api.serializers import CarCreateSerializer, CarSerializer, CarPopularSerializer, RateSerializer

client = Client()

class GetAllCarsTest(TestCase):

    def setUp(self):
        Car.objects.create(make='Volkswagen', model='Golf')
        Car.objects.create(make='Ford', model='Focus')
        Car.objects.create(make='Opel', model='Corsa')
        Car.objects.create(make='Audi', model='A8')

    def test_get_all_cars(self):
        response = client.get(reverse('cars'))
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class DeleteSingleCarTest(TestCase):

    def setUp(self):
        self.vw = Car.objects.create(make='Volkswagen', model='Golf')
        self.ford = Car.objects.create(make='Ford', model='Focus')

    def test_valid_delete_car(self):
        response = client.delete(reverse('car', kwargs={'pk': self.vw.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_puppy(self):
        response = client.delete(reverse('car', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewCarTest(TestCase):

    def setUp(self):
        self.valid_payload = {
            'make': 'Volkswagen', 
            'model': 'Golf'
        }
        self.invalid_payload_no_make = {
            'make': '', 
            'model': 'Golf'
        }
        self.invalid_payload_part_make = {
            'make': 'wagen', 
            'model': 'Golf'
        }
        self.invalid_payload_wrong_model = {
            'make': 'Volkswagen', 
            'model': 'Golfxx'
        }


    def test_create_valid_car(self):
        response = client.post(
            reverse('cars'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_car_no_make(self):
        response = client.post(
            reverse('cars'),
            data=json.dumps(self.invalid_payload_no_make),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_car_part_make(self):
        response = client.post(
            reverse('cars'),
            data=json.dumps(self.invalid_payload_part_make),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_car_wrong_model(self):
        response = client.post(
            reverse('cars'),
            data=json.dumps(self.invalid_payload_wrong_model),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class GetMostPopularCarsTest(TestCase):

    def setUp(self):
        Car.objects.create(make='Volkswagen', model='Golf', avg_rating=1, rates_number=4)
        Car.objects.create(make='Ford', model='Focus', avg_rating=2, rates_number=2)
        Car.objects.create(make='Opel', model='Corsa', avg_rating=4.25, rates_number=8)
        Car.objects.create(make='Audi', model='A8', avg_rating=4.25, rates_number=60)

    def test_get_all_cars(self):
        response = client.get(reverse('popular-cars'))
        cars = Car.objects.all().order_by('-rates_number')[:10]
        serializer = CarPopularSerializer(cars, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CreateNewRateTest(TestCase):

    def setUp(self):
        self.vw = Car.objects.create(make='Volkswagen', model='Golf', avg_rating=4.25, rates_number=4)
        self.valid_payload = {
            'car_id': self.vw.pk, 
            'rating': 4
        }
        self.invalid_payload = {
            'car_id': self.vw.pk, 
            'rating': 88
        }

    def test_create_valid_rate(self):
        response = client.post(
            reverse('rates'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.vw.refresh_from_db()
        self.assertEqual(5, self.vw.rates_number)
        self.assertEqual(4.2, self.vw.avg_rating)

    def test_create_invalid_(self):
        response = client.post(
            reverse('rates'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
