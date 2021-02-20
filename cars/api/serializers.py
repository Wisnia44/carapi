from rest_framework import serializers
from cars.models import Car, Rate

class CarCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Car
		fields = [
			'make',
			'model',
		]

class CarSerializer(serializers.ModelSerializer):
	class Meta:
		model = Car
		fields = [
			'id',
			'make',
			'model',
			'avg_rating',
		]

class CarPopularSerializer(serializers.ModelSerializer):
	class Meta:
		model = Car
		fields = [
			'id',
			'make',
			'model',
			'rates_number',
		]

class RateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Rate
		fields = [
			'car_id',
			'rating',
		]
		extra_kwargs = {
            'rating': {'min_value': 1, 'max_value': 5},
        }
