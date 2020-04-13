from django.urls import path
from django.conf.urls import url

from .views import (
    index, registration, profile, login_request, logout_request,
    activate, resend_activation_link
    )

app_name = 'opinion_aggregator'

urlpatterns = [
    path('', index, name='index'),
    path('register', registration, name='register'),
    path('profile', profile, name='profile'),
    path('login', login_request, name='login'),
    path('logout', logout_request, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('resend_activation/<str:email>', resend_activation_link, name='resend_activation')
]