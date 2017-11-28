from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question, Choice
from django.db.models import F


class IndexView(generic.ListView):
    template_name = 'stock/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'stock/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'stock/results.html'

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'stock/results.html', context={"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'stock/detail.html', {'question': question, 'error_message': "You Don't selected a choic"})
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('stock:results', args=(question.id,)))