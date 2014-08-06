from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from home.models import Signup

def submit_form(request, user_id):
    user = Signup.objects.get(id=user_id)
    if request.session.get('signed_up', False):
        email = user.email
        messages.add_message(request, messages.INFO, 'Thanks!')
        send_mail('Thanks!', 'test', 'noreply@mydailyfit.com', [email], fail_silently=False)
        del request.session['signed_up']
        return HttpResponseRedirect(reverse('home:index'))
    else:
        messages.add_message(request, messages.ERROR, 'Session not set')
        return HttpResponseRedirect(reverse('home:index'))
