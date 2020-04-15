from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'opinion_aggregator'

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.registration, name='register'),
    path('profile', views.profile, name='profile'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('resend_activation/<str:email>', views.resend_activation_link, name='resend_activation'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('survey', views.survey, name='survey'),
    path('analytics', views.analytics, name='analytics'),
    path('contact', views.contact, name='contacnt')
]