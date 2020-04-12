from django.urls import path

from .views import index, registration, profile

app_name = 'opinion_aggregator'

urlpatterns = [
    path('', index, name='index'),
    path('register', registration, name='register'),
    path('profile', profile, name='profile')
]