from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from opinion_aggregator.forms import UserRegistrationForm
from opinion_aggregator.utils import send_email


# Create your views here.

def index(request):
    """renders the homepage

    Arguments:
        request {object} -- django http object
    """
    return render(request, 'index.html')


def registration(request):
    """renders the registration page
    and allows a user to create a profile

    Arguments:
        request {object} -- django http object
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            auth_login(request, user)
            message = "Welcome! You have successfuly created an account"
            send_email("youthforuae@gmail.com", user.email, message)
            return redirect('/profile')
        else:
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