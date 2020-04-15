import os
import base64
from django.conf import settings
from django.forms import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from opinion_aggregator.forms import UserRegistrationForm, LoginForm, EditProfileForm
from opinion_aggregator.utils import send_email
from opinion_aggregator.token import account_activation_token
from opinion_aggregator.models import User, QuestionModel, SurveyResponsesModel
from opinion_aggregator.dao.survey import get_surveys, get_survey_parts, get_survey_sections
from opinion_aggregator.dao.survey import get_surveys, get_survey_parts, get_user_responses
from opinion_aggregator.utils.email import send_email
from opinion_aggregator.utils import create_service_account


# Create your views here.

def login_request(request):
    """renders the homepage

    Arguments:
        request {object} -- django http object
    """
    login_form = LoginForm()
    context = {'form': login_form}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return authenticate_user(request)
        error_message = "Invalid credentials, check your input and try again!"
        messages.error(request, error_message, extra_tags='red darken-1')
        return redirect('/')
    error_message = "Please login to perfom this action"
    messages.error(request, error_message, extra_tags='red darken-1')
    return render(request, 'index.html', context)


def authenticate_user(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            next_page = request.POST.get('next')
            if next_page:
                message = "Welcome {}!".format(user.email)
                messages.success(request, message, extra_tags='green')
                return redirect(next_page)
            message = "Welcome {}!".format(user.email)
            messages.success(request, message)
            return redirect('/')
        error_message = "That account has not yet been activated"
        messages.error(request, error_message, extra_tags='red darken-1')
        return render(request, 'auth/activate_account.html', {'email': user.email})
    error_message = "Invalid email/password combination!"
    messages.error(request, error_message, extra_tags='red darken-1')
    return redirect('/')


def index(request):
    """render the index page
    """
    return render(request, 'index.html', {'form': LoginForm()})

def registration(request):
    """renders the registration page
    and allows a user to create a profile

    Arguments:
        request {object} -- django http object
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            create_service_account()
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            # form.send_email(request, user)
            return render(request, 'registration_success.html', {'email': user.email})
        else:
            error_message = "Please correct the errors below and try again!"
            messages.error(request, error_message, extra_tags='red darken-1')
            return render(request, 'registration.html', {'form': form})
    registration_form = UserRegistrationForm()
    context = {
        'form': registration_form,
        }
    return render(request, 'registration.html', context)

@login_required
def profile(request):
    """renders the profile page
    """
    return render(request, 'profile.html')


def logout_request(request):
    """Terminates user session"""
    login_form = LoginForm()
    context = {'form': login_form}
    if request.user:
        logout(request)
        message = "Successfuly logged out!"
        messages.success(request, message, extra_tags='green')
        return redirect('/', context)


def activate(request, uidb64, token):
    """Set user activation status to true."""
    user = UserRegistrationForm().get_user(uidb64)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        return redirect('/profile')
    return render(request, 'auth/signup_activation_invalid.html')


def resend_activation_link(request, email):
    if email:
        user = User.objects.get(email=email)
        UserRegistrationForm().send_email(request, user)
        message = "A new link has been sent to your inbox"
        messages.success(request, message, extra_tags='green')
        return render(request, 'index.html', {'form': LoginForm()})
    return redirect('/register')


@login_required(login_url="/login")
def edit_profile(request):
    """edit user profile
    """
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            return clean_password(form, request)
        return render(request, 'edit_profile.html', {'form': form})
    return render(request, 'edit_profile.html', {'form': EditProfileForm()})


def clean_password(form, request):
    user = request.user
    cleaned_data = request.POST
    password = cleaned_data['password']
    if password and (not password.isspace()):
        if not user.check_password(password):
            error_message = "Wrong password!"
            messages.error(request, error_message, extra_tags='red darken-1')
            return redirect('/edit_profile')
        return save_user(form, request)


def save_user(form, request):
    create_service_account()
    cleaned_data = form.cleaned_data
    del cleaned_data['password']
    User.objects.filter(pk=request.user.pk).update(**cleaned_data)
    return redirect('/profile')


@login_required(login_url="/login")
def survey(request):
    """render a survey
    """
    if request.method == 'POST':
        return save_response(request)
    surveys = get_surveys()
    survey_parts = get_survey_parts()
    page = request.GET.get('page', 1)

    paginator = Paginator(survey_parts, 1)
    try:
        parts = paginator.page(page)
    except PageNotAnInteger:
        parts = paginator.page(1)
    except EmptyPage:
        parts = paginator.page(paginator.num_pages)

    context = {
        'surveys': surveys,
        'parts': parts
    }
    return render(request, 'survey.html', context)


def save_response(request):
    """save user response
    """
    user = request.user
    cleaned_data = request.POST
    mutable_data = cleaned_data.copy()
    del mutable_data['csrfmiddlewaretoken']
    del mutable_data['action']
    for key, value in mutable_data.items():
        question = QuestionModel.objects.filter(pk=int(key)).first()
        if value and (not value.isspace()):
            SurveyResponsesModel.objects.create(
                response=value, user=user, question=question)
    message = "Thank you for your response"
    messages.success(request, message, extra_tags='green')
    return redirect('/survey#pagination')


def analytics(request):
    """render response analysis
    """
    context = {
        'sections': get_survey_sections
    }
    return render(request, 'analytics.html', context)
def contact(request):
    if request.method == "POST":
        cleaned_data = request.POST
        firstname = cleaned_data['firstname']
        email = cleaned_data['email']
        message = cleaned_data['email_msg']
        send_email("My voice", email, settings.EMAIL_HOST_USER, message)
        success = "Your message has been recorded, we will contact you soon"
        messages.success(request, success, extra_tags='green')
        return redirect('/')
    return render(request, 'contact.html')


@login_required(login_url="/login")
def view_personal_responses(request):
    user = request.user
    responses = get_user_responses(user)
    context = {
        'responses': responses
    }
    return render(request, 'user_responses.html', context)