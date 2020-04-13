import re
from django.contrib.sites.shortcuts import get_current_site
from django import forms
from django.core.files import File
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from opinion_aggregator.models import User, CountryCode, get_default
from opinion_aggregator.token import account_activation_token


class LoginForm(forms.Form):
    """
    Login form
        - Authenticates user agains registered accounts
    """
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """
    Registration form
        - Collects user information for account creation
    """
    class Meta:
        model = User
        fields = ('email', 'firstname', 'lastname', 'address', 'phone_number', 'date_of_birth', 'gender', 'photo')

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def clean_password2(self):
        """
        Validate passwords match
        """
        cleaned_data = self.cleaned_data
        password = cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError('Password must be more than eight characters')
        elif re.search('[0-9]',password) is None:
            raise forms.ValidationError('Make sure your password has a number in it')
        if password != cleaned_data['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cleaned_data['password2']

    def save(self, commit=True):
        """
        Save user to the database.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def send_email(self, request, user):
        """
        Send email to user after successful registration.
        parameters:
            request(object): Contains metadata about the request
            user(object): Object representing the user requesting for
            registration
        """
        current_site = get_current_site(request)
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }
        to_email = user.email
        subject = loader.render_to_string(
            "auth/activation_subject.txt", context
            )
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(
            "auth/account_activation.html", context
            )
        email_message = EmailMultiAlternatives(subject, body, None, [to_email])
        email_message.content_subtype = "html"
        email_message.send()

    def get_user(self, uidb64):
        """
        Return a user object based on the user's id encoded in base 64.
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user
