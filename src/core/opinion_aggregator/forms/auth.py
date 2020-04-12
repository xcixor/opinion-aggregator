import re
from django import forms
from opinion_aggregator.models import User, CountryCode, get_default


class LoginForm(forms.Form):
    """
    Login form
        - Authenticates user agains registered accounts
    """
    username = forms.CharField()
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