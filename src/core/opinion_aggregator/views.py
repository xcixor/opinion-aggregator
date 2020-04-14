import subprocess
import os
import base64
from django.forms import ValidationError
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from opinion_aggregator.forms import UserRegistrationForm, LoginForm, EditProfileForm
from opinion_aggregator.utils import send_email
from opinion_aggregator.token import account_activation_token
from opinion_aggregator.models import User


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
        create_service_account()
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            form.send_email(request, user)
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


def create_service_account():
    """create service account
    """
    # print(os.environ.get('DJANGO_SETTINGS_MODULE'), '******settings**********')
    service_account_data = os.environ.get('SERVICE_ACCOUNT')
    account_data = base64.b64decode(service_account_data)
    data = account_data.decode('ascii')
    base_dir = settings.BASE_DIR
    root_dir = base_dir[:-13]
    filename = "{}/account.json".format(root_dir)
    with open(filename, "w") as f:
        f.write(data)

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
        messages.error(request, message, extra_tags='green')
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


@login_required
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
    cleaned_data = form.cleaned_data
    del cleaned_data['password']
    User.objects.filter(pk=request.user.pk).update(**cleaned_data)
    return redirect('/profile')