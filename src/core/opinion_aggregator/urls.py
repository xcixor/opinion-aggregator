from django.urls import path

from .views import index

app_name = 'opinion_aggregator'

urlpatterns = [
    path('', index, name='index'),
]