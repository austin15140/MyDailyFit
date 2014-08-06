from django.shortcuts import render
from datetime import datetime
from forms import NewUser
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from models import Signup

def index(request):
    year = datetime.now().year
    c_name = 'mydailyfit'
    new_form = NewUser()
    if request.method == 'POST':
        new_form = NewUser(request.POST)
        if new_form.is_valid():
            email = request.POST['email']
            user = Signup.objects.create(email=email)
            user.save()
            request.session['signed_up'] = True
            return HttpResponseRedirect(reverse('signups:email', args=(user.id,)))
        else:
            messages.add_message(request, messages.ERROR, new_form.errors)
            new_form = NewUser()
    context = {'year': year, 'c_name': c_name, 'new_form': new_form}
    return render(request, 'home/index.html', context)