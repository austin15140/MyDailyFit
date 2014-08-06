from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core import serializers

#from core.util_functions import attempt_login, create_new_user

from .forms import UserForm, NewUser, LoginForm, FileForm, SearchForm, UserInfo
from .models import UserProfile, UserFile


# View for the home page
def index(request):
    new_user = NewUser()
    login_form = LoginForm()
    search_form = SearchForm()
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            choice1 = request.POST['goal']
            choice2 = request.POST['age']
            if choice1 == 'goal':
                choice1 = 'lose_weight'
            if choice2 == 'age':
                choice2 = '18-29'
            messages.add_message(request, messages.INFO, choice1 + choice2)
            context = {'search_form': search_form, 'new_user': new_user, 'login_form': login_form}
            return render(request, 'users/index.html', context)
        else:
            messages.add_message(request, messages.INFO, search_form.errors)
    context = {'search_form': search_form, 'new_user': new_user, 'login_form': login_form}
    return render(request, 'users/index.html', context)

# View for the page used to browse through Personal Trainers
def browse(request):
    login_form = LoginForm()
    new_user = NewUser()
    search_form = SearchForm()
    if request.method == 'POST':
        if search_form.is_valid():
            context = {'login_form': login_form, 'new_user': new_user}
            return render(request, 'users/browse.html', context)
        else:
            form_errors = search_form.errors
            messages.add_message(request, messages.INFO, search_form.errors)
            return HttpResponseRedirect(reverse('users:index'))
    context = {'login_form': login_form, 'new_user': new_user}
    return render(request, 'users/browse.html', context)

"""
** NOT A VIEW **
"""
# This function is used to create a new User object if the
# form that was submitted is valid
def new_user(request):
    new_user = NewUser()
    loginform = LoginForm()
    # Make sure the form was POSTed
    if request.method == 'POST':
        new_user = NewUser(request.POST)
        if new_user.is_valid():
            # Grab the user's input and check it against current User objects in database
            # If an inputted value is already stored in the database, raise a ValidationError
            if new_user.check_email() and new_user.check_username():
                # If both checks pass, create the new User
                new_user.create_new_user()
            # If the a check fails, display an error message
            elif not new_user.check_email():
                messages.add_message(request, messages.INFO, 'The e-mail you entered is already associated with an account on file.')
            elif not new_user.check_username():
                messages.add_message(request, messages.INFO, 'The username you entered is already associated with an account on file.')
        # Display error message and redirect if form validation fails
        else:
            form_errors = new_user.errors
            messages.add_message(request, messages.INFO, form_errors)
            return HttpResponseRedirect(reverse('users:new_user'))
    context = {'new_user': new_user, 'login_form': loginform}
    return render(request, 'users/signup.html', context)

# This view handles the home page directed towards Personal Trainers
# Also includes the LoginForm and NewUser form
def personal_trainer(request):
    new_user = NewUser()
    login_form = LoginForm()
    context = {'new_user': new_user, 'login_form': login_form}
    return render(request, 'users/pt.html', context)

# Used to display the User's Profile page
def detail(request, username):
    # Grab the associated User object
    user = get_object_or_404(User, username=username)
    # Grab the associated UserProfile object
    userprofile = get_object_or_404(UserProfile, user=user.id)
    # Create a JSON Serializer so we can access data related
    #  to this User object with JavaScript
    json_serializer = serializers.get_serializer('json')()
    all_users = json_serializer.serialize(User.objects.all().filter(username=username))
    context = {'user': user, 'all_users': all_users, 'userprofile': userprofile}
    return render(request, 'users/profile.html', context)

"""
This is used to help me remember how to make an image downloadable in python
"""
def download_img(request, photo):
    photo = get_object_or_404(User, photo=photo)
    fsock = open(photo.name, 'r')
    response = HttpResponse(fsock, mimetype='image/jpeg')
    response['Content-Disposition'] = "attachment; filename=%s" % photo.name
    return response

# View that handles the User's account including all settings and their Fitness Track
def account(request, username):
    user = get_object_or_404(User, username=username)
    user_id = user.id
    userprofile = get_object_or_404(UserProfile, user=user_id)
    userinfo = UserInfo(initial={'tagline': userprofile.tagline, 'location': userprofile.location, 'weight': userprofile.weight, 'age': userprofile.age})
    if request.method == 'POST':
        userinfo = UserInfo(request.POST, request.FILES)
        if userinfo.is_valid():
            userinfo.process_and_save(username)
            return HttpResponseRedirect(reverse('users:detail', args=[user.username]))
        else:
            messages.add_message(request, messages.INFO, 'Something went wrong. Please try again.')
    context = {'userprofile': userprofile, 'user': user, 'userinfo': userinfo}
    return render(request, 'users/account.html', context)

# View that handles authenticating and logging in a User
def user_login(request):
    loginform = LoginForm()
    new_user = NewUser()
    # Initialize variables with empty string
    invalid = ''
    disabled = ''
    # Make sure that the form was POSTed
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            # Grab the submitted values
            username = request.POST['username']
            password = request.POST['password']
            # Attempt to grab a User object with submitted credentials
            user = authenticate(username=username, password=password)
            # If a User object was returned and the User is active,
            # log in the user and redirect the User to their profile page
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('users:detail', args=(user.username,)))
                # If the User is not active, display an error message and send them to the
                # login page
                else:
                    disabled = 'User is not active'
                    context = {'loginform': loginform, 'invalid': invalid, 'disabled': disabled}
                    return render(request, 'users/login.html', context)
            # If no User object was returned, display an error message and send them to the
            # login page
            else:
                messages.add_message(request, messages.INFO, 'The username or password you entered is incorrect. Please try again.')
                context = {'loginform': loginform, 'disabled': disabled, 'new_user': new_user}
                return render(request, 'users/login.html', context)
        # If the form is not valid, display an error message and send them to the
        # login page
        else:
            messages.add_message(request, messages.INFO, "In order to login, you must complete the form.")
            context = {'loginform': loginform, 'disabled': disabled, 'new_user': new_user}
            return render(request, 'users/login.html', context)
    # If the form was not POSTed, refresh the LoginForm and send them to the
    # login page
    else:
        loginform = LoginForm()
        context = {'loginform': loginform, 'invalid': invalid, 'disabled': disabled, 'new_user': new_user}
        return render(request, 'users/login.html', context)

# View that handles logging out a User
def user_logout(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'You have been successfully logged out.')
    return HttpResponseRedirect(reverse('users:index'))
