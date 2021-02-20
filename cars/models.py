from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Car(models.Model):
	make = models.CharField(max_length=50)
	model = models.CharField(max_length=50)
	avg_rating = models.FloatField(default=0)
	rates_number = models.PositiveSmallIntegerField(default=0)
	# I assume that GET Car/Cars would be called more frequently that POST Rate
	# so the solution where avg_ratings and rates_number is part of Car model is optimal

class Rate(models.Model):
	car_id = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
	rating = models.PositiveSmallIntegerField(
		validators=[
			MaxValueValidator(100),
			MinValueValidator(1)
			]
		)
