from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.context_processors import csrf
from quiz.models import *
from quiz.forms import *

def questions_list(request):
	questions = MultipleChoice.objects.all()
	return render_to_response('quiz/question_list.html', {'questions': questions })

def question(request, id, slug):
	question = MultipleChoice.objects.get(pk=id)
	return render_to_response('quiz/question.html', {'question': question })

def create_quiz(request, id):
	# todo: put this as a form
	quiz = Quiz.objects.get(pk=id)
	quiz_instance = QuizInstance(taker=request.user, quiz=quiz)
	quiz_instance.save()
	return redirect('quiz', id=quiz_instance.pk)


def quiz(request, id):
	question_number = 0
	quiz_instance = QuizInstance.objects.get(pk=id)
	quiz = quiz_instance.quiz
	if request.method == 'POST':
		# save response
		post_data = request.POST
		question_number = int(post_data['question_number']) + 1
		if question_number >= quiz.question_count:
			# compute score and results
			score = 5
			c = {'score': score }
			c.update(csrf(request))
			return render_to_response('quiz/quiz_finished.html', c)
	question = quiz.get_question(question_number)
	quiz_form = QuizForm(question)
	# todo: garble question_number using a combination of a key, question, quiz and quiz instance
	c = {'q': question, 'question_form' : quiz_form, 'question_number': question_number }
	c.update(csrf(request))
	return render_to_response('quiz/quiz.html', c)
