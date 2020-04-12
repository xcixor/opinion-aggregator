from django.shortcuts import render

# Create your views here.

def index(request):
    """renders the homepage

    Arguments:
        request {object} -- django http object
    """
    return render(request, 'index.html')


def registration(request):
    """renders the registration page

    Arguments:
        request {object} -- django http object
    """
    return render(request, 'registration.html')