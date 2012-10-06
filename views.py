from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.utils import timezone
from quiz.models import *
from quiz.forms import *

def create_user_response(user_response, answers):
	user_response.response=[MultipleChoiceAnswer.objects.get(pk=x) for x in answers]	
	user_response.save()



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
	# todo: check if instance already exists, retrieve it
	quiz_instance.save()
	return HttpResponseRedirect(reverse('quiz.views.quiz', args=(quiz_instance.pk,)))


def quiz(request, id):
	question_number = 0
	quiz_instance = QuizInstance.objects.get(pk=id)
	quiz = quiz_instance.quiz
	if request.method == 'POST':
		# save response
		post_data = request.POST
		print post_data
		question_id = int(post_data['question_number'])
		user_response = UserResponse(quiz_instance=quiz_instance, question=quiz.get_question(question_id), time_taken_delta = timezone.now())
		user_response.save()
		create_user_response(user_response, post_data['choices'])
		question_number =  question_id + 1
		if question_number >= quiz.question_count:
			# compute score and results
			quiz_instance.score = sum([int(x.is_correct) for x in quiz_instance.get_responses])
			# set quiz instance status to complete
			quiz_instance.save()
			c = {'score': quiz_instance.score }
			c.update(csrf(request))
			return render_to_response('quiz/quiz_finished.html', c)
	question = quiz.get_question(question_number)
	quiz_form = QuizForm(question)
	# todo: garble question_number using a combination of a key, question, quiz and quiz instance
	c = {'q': question, 'question_form' : quiz_form, 'question_number': question_number }
	c.update(csrf(request))
	return render_to_response('quiz/quiz.html', c)

def result(request, id):
	quiz_instance = QuizInstance.objects.get(pk=id)
	# if object is not found, return 404, probably use a monad
	# if quiz is not in completed status, return 404
	return render_to_response('quiz/quiz_finished.html', {'score': quiz_instance.score })
	
