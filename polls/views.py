from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import generic
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from polls.models import Poll, Choice
from polls.forms import PollForm, ChoiceForm, DelPollForm

def index(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    pollform = PollForm()
    choiceform = ChoiceForm()
    if request.method == 'POST':
        pollform = PollForm(request.POST, request.FILES)
        choiceform = ChoiceForm(request.POST)
        if pollform.is_valid():
            pollform.comments = pollform.cleaned_data['comments']
            pollform.save()
        else:
            pollform = PollForm()
        if choiceform.is_valid():
            choiceform.save()
        else:
            choiceform = ChoiceForm()
    context = {'latest_poll_list': latest_poll_list, 'pollform': pollform,
               'choiceform': choiceform}
    return render(request, 'polls/index.html', context)

def deletePoll(request, pk):
    p = get_object_or_404(Poll, pk=pk)
    d = p.id
    delform = DelPollForm({'question': p,})
    if request.method == 'POST':
        delform = DelPollForm(request.POST)
        if delform.is_valid():
            p.delete()
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            delform = DelPollForm()
    context = {'delform': delform, 'd': d, 'p': p,}
    return render(request, 'polls/del.html', context)

'''
def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/detail.html', {'poll': poll})

def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': p})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return Poll.objects.order_by('-pub_date')[:5]
'''
class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': 'You didn\'t select a choice.'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def dummy(request, dummytxt):
    return HttpResponse("Just some dummy text: %s" % dummytxt)