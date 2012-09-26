from django.shortcuts import render_to_response, get_object_or_404
from quiz.models import *

def questions_list(request):
	questions = MultipleChoice.objects.all()
	return render_to_response('quiz/question_list.html', {'questions': questions })

def question(request, id, slug):
	question = MultipleChoice.objects.get(pk=id)
	return render_to_response('quiz/question.html', {'question': question })

def quiz(request, id):
	pass
