from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from users.models import UserProfile, get_randfile_path, UserFile

my_default_errors = {
    'required': ' -\tThis field is required\n',
    'invalid': ' -\tEnter a valid value\n'
}

class UserForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))
    class Meta:
        model = UserProfile
        exclude = {'user', 'description'}

class NewUser(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

# Use check_username to make sure that there are no existing users with the same username
# *** Raise a ValidationError if there is already a user with same username ***
#
    def check_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
            if User:
                return False
        except User.DoesNotExist:
            return self.cleaned_data['username']

# Use check_email to make sure that there are no existing users with the same email addres
# *** Raise a ValidationError if there is already a user with same email address ***
#
    def check_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
            if User:
                return False
        except User.DoesNotExist:
            return self.cleaned_data['email']

# Perform the first two validation checks to make sure username and email are OK to use for a new user
# If checks pass, create new user with the submitted data
    def create_new_user(self):
        username = self.check_username()
        email = self.check_email()
        new_user = User.objects.create_user(username=username, email=email, password=self.cleaned_data['password'])
        # Add the first and last name to the user
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        # Save this new user in the database
        new_user.save()

# Form for logging in and authorizing a User
class LoginForm(forms.Form):
    username = forms.CharField(error_messages=my_default_errors, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control m-t-2', 'placeholder': 'Username'}))
    password = forms.CharField(error_messages=my_default_errors, max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control m-t-2', 'placeholder': 'Password'}))


class SearchForm(forms.Form):
    AGES = (
        ('age', 'Select your age'),
        ('18-29', '18-29'),
        ('29-39', '29-39'),
        ('39-49', '39-49'),
        ('50+', '50+'),
    )
    GOALS = (
        ('goal', 'Select your goal'),
        ('lose_weight', 'Lose Weight'),
        ('gain_muscle', 'Gain Muscle'),
        ('gain_weight', 'Gain Weight'),
    )
    goal = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=GOALS)
    age = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=AGES)

# Form for updating Tagline, Profile, and Background Image
class UserInfo(forms.Form):
    prof_img = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'file-input', 'id': 'file1'}))
    bg_img = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'file-input2', 'id': 'file2'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Charlotte, NC'}))
    weight = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Weight in pounds e.g. 180'}))
    age = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Age in years e.g. 32'}))
    tagline = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Briefly explain your goal for others to see'}))

    # Define a method to process and save the form
    def process_and_save(self, username):
        # Grab the current User object and assign its ID to a variable
        user = get_object_or_404(User, username=username)
        user_id = user.id
        # Grab the UserProfile object associated with the current User
        userprofile = get_object_or_404(UserProfile, user=user_id)
        # Grab the inputted data
        bg_img = self.cleaned_data.get('bg_img', userprofile.bg_img)
        prof_img = self.cleaned_data.get('prof_img', userprofile.prof_img)
        tagline = self.cleaned_data.get('tagline', userprofile.tagline)
        location = self.cleaned_data.get('location', userprofile.location)
        weight = self.cleaned_data.get('weight', userprofile.weight)
        age = self.cleaned_data.get('age', userprofile.age)
        # If the current UserProfile's field is not equal to what was submitted
        # Update the UserProfile with the submitted data
        if not bg_img:
            pass
        elif bg_img != userprofile.bg_img:
            userprofile.bg_img = bg_img
        if not prof_img:
            pass
        elif prof_img != userprofile.prof_img:
            userprofile.prof_img = prof_img
        if tagline != userprofile.tagline:
            userprofile.tagline = tagline
        if weight != userprofile.weight:
            userprofile.weight = weight
        if age != userprofile.age:
            userprofile.age = age
        if location != userprofile.location:
            userprofile.location = location
        # Save the changes that were made to the UserProfile
        userprofile.save()

class FileForm(forms.ModelForm):
    class Meta:
        model = UserFile

class Del_Video(forms.Form):
    Delete = forms.BooleanField()

class Del_File(forms.Form):
    Delete = forms.BooleanField()

class Del_Photo(forms.Form):
    Delete = forms.BooleanField()