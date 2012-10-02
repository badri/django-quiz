from django import forms

from quiz.models import *
'''
class QuestionForm(forms.Form):
	answers = forms.ChoiceField(widget=forms.RadioSelect(), label=u"Please select a answer:")
	
	def __init__(self, question, *args, **kwargs):
		super(QuestionForm, self).__init__(*args, **kwargs)
		self.question = question
		answers = question.answers.order_by('weight')
		self.fields['answers'].choices = [(i, a.answer) for i, a in enumerate(answers)]
		
		for pos, answer in enumerate(answers):
			if answer.id == question.correct_answer_id:
				self.correct = pos
			break
	
	def is_correct(self):
		if not self.is_valid():
			return False
		
		return self.cleaned_data['answers'] == str(self.question.correct_answer.id)

def quiz_forms(quiz, data=None):
	questions = Question.objects.filter(quiz=quiz).order_by('id')
	form_list = []
	for pos, question in enumerate(questions):
		form_list.append(QuestionForm(question, data, prefix=pos))
	return form_list
'''

class QuizForm(forms.Form):
	choices = forms.ModelChoiceField(queryset=MultipleChoiceAnswer.objects.none(),
					 widget=forms.CheckboxSelectMultiple, required=True, show_hidden_initial=True)

	def __init__(self, question):
		super(QuizForm, self).__init__()
		self.fields['choices'].queryset = question.choices.all()
		self.fields['choices'].empty_label = None

class QuizForm2(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuizForm2, self).__init__(*args, **kwargs)
        self.fields['choices'] = forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices=[ (x.id, x.answer) for x in question.choices.all()])
