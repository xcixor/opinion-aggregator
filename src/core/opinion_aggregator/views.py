from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from opinion_aggregator.forms import UserRegistrationForm, LoginForm
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
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(
                request,
                email=email,
                password=password
                )
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
                else:
                    error_message = "That account has not yet been activated"
                    messages.error(request, error_message, extra_tags='red darken-1')
                    return render(request, 'auth/activate_account.html', {'email': user.email})
            else:
                error_message = "Invalid email/password combination, Please try Again!"
                messages.error(request, error_message, extra_tags='red darken-1')
                return redirect('/')
        else:
            error_message = "Invalid Credentials, Please try Again!"
            messages.error(request, error_message, extra_tags='red darken-1')
            return redirect('/')
    else:
        form = LoginForm()
    msg = "You need to be logged in to perform this action!"
    messages.error(request, msg, extra_tags='red darken-1')
    return render(request, 'index.html', context)

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
        return render(request, 'index.html', {'form': LoginForm()})
    return redirect('/register')
