from django import forms
from polls.models import Poll, Choice
from django.forms.extras.widgets import SelectDateWidget

class PollForm(forms.ModelForm):
    #pub_date = forms.DateField(widget=SelectDateWidget)
    comments = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 10}))
    class Meta:
        model = Poll

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice

class DelPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        exclude = ['comments', 'image']