from django.urls import path
from django.conf.urls import url
from .views import get_post_cars, delete_car, post_rate, get_popular_cars

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
	openapi.Info(
		title="Docs CarAPI",
		default_version='v1',
		description="CarAPI Documentation",
		terms_of_service="https://www.google.com/policies/terms",
		contact=openapi.Contact(email="contact@snippets.local"),
		license=openapi.License(name="BSD License"),
		),
	public=True,
	permission_classes=[permissions.AllowAny],
	)

urlpatterns = [
	path('cars/', get_post_cars, name='cars'),
	path('car/<int:pk>/', delete_car, name='car'),
	path('rate/', post_rate, name='rates'),
	path('popular/', get_popular_cars, name='popular-cars'),
	url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
	url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
	path('', schema_view.with_ui('redoc', cache_timeout=0), name='index'),
]
