__author__ = 'austinbailey'
from django import forms

my_default_errors = {
    'required': ' -\tThis field is required\n',
    'invalid': ' -\tEnter a valid value\n'
}

class NewUser(forms.Form):
    email = forms.EmailField(error_messages=my_default_errors,
                             widget=forms.TextInput(attrs={'placeholder': 'Email address', 'class': 'form-control', 'id': 'email',
                                                           'rel': 'tooltip', 'title': 'Don\'t worry, we won\'t spam you'}))