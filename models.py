'''
TODO
1. add subjective and true or false questions
2. time per question and time for overall quiz
3. quiz settings
4. change order
5. repoduce a quiz already taken
6. garble form hidden values
7. change correct answer selection for a question.
8. business rules
9. quiz status
10. question explanaiton
'''

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatewords_html
from quiz.managers import *
from quiz.exceptions import ScoreTamperedException

class Category(models.Model):
	"""Category model."""
	title = models.CharField(_('title'), max_length=100)
	slug = models.SlugField(_('slug'), unique=True)

	class Meta:
		verbose_name = _('category')
		verbose_name_plural = _('categories')
		db_table = 'quiz_categories'
		ordering = ('title',)

	def __unicode__(self):
		return u'%s' % self.title

        @permalink
        def get_absolute_url(self):
		return ('quiz_category_detail', None, {'slug': self.slug})


class MultipleChoiceAnswer(models.Model):
	'''A multichoice answer.'''
	answer = models.TextField(_('answer'))

	def __unicode__(self):
		return u"%s" % truncatewords_html(self.answer, 10)


class MultipleChoice(models.Model):
	'''Multiple choice question with answer choices.'''
	question = models.TextField(_('question'))
	slug = models.SlugField(_('slug'))
	choices = models.ManyToManyField(MultipleChoiceAnswer)
	correct_answer = models.ManyToManyField(MultipleChoiceAnswer, related_name="correct", blank=True) #can have more than 1 correct answer, can be blank
	categories = models.ManyToManyField(Category, blank=True)

	def __unicode__(self):
		return u"%s" % truncatewords_html(self.question, 10)

        @permalink
        def get_absolute_url(self):
		return ('quiz.views.question', [self.pk, self.slug])

	
class Quiz(models.Model):
	'''A quiz template.'''
	STATUS_CHOICES = (
		(1, _('Draft')),
		(2, _('Public')),
		(3, _('Close')),
	)

	FEEDBACK_CHOICES = (
		(1, _('At the end of the quiz')),
		(2, _('After each question')),
		(3, _('Don\'t disclose')),
	)
	setter = models.ForeignKey(User, related_name='setter')
	title = models.CharField(_('title'), max_length=100)
	slug = models.SlugField(_('slug'))
	description = models.TextField(_('description'), blank=True, null=True)	
	status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1)
	questions = models.ManyToManyField(MultipleChoice)
	categories = models.ManyToManyField(Category, blank=True)	
	published = models.DateTimeField(_('published'))	
	date_added = models.DateTimeField(_('date added'), auto_now_add=True)
	date_modified = models.DateTimeField(_('date modified'), auto_now=True)

	allow_skipping = models.BooleanField(default=False)
	allow_jumping = models.BooleanField(default=False)
	backwards_navigation = models.BooleanField(default=False)
	random_question = models.BooleanField(default=False) # conditional
	feedback = models.IntegerField(_('feedback'), choices=FEEDBACK_CHOICES, default=1)
	multiple_takes = models.BooleanField(default=False) # conditional	
	
	class Meta:
		verbose_name = _('quiz')
		verbose_name_plural = _('quizzes')
		db_table = 'quizzes'
		ordering = ('-published',)
	
	def __unicode__(self):
		return u"%s" % self.title
	
	@property
	def question_count(self):
		return len(self.questions.all())

	def get_question(self, id):
		return self.questions.all()[id]


class QuizInstance(models.Model):
	'''A combination of user response and a quiz template.'''
	taker = models.ForeignKey(User)
	quiz = models.ForeignKey(Quiz)
	quiz_taken = models.DateTimeField(_('quiz taken'), auto_now_add=True)
	score = models.IntegerField(default=0)
	
	# prevent from setting score in the frontend to avoid tampering
	def __setattr__(self, name, value):
		if name == 'score':
			if getattr(self, 'score', None):
				if getattr(self, 'score') != 0:
					raise ScoreTamperedException(self.quiz, self.quiz.id, value)
		super(QuizInstance, self).__setattr__(name, value)

	def __unicode__(self):
		return u"%s, taken by %s on %s" % (self.quiz, self.taker, self.quiz_taken.strftime("%A, %d %B %Y %I:%M%p"))

	@property
	def get_responses(self):
		return UserResponse.objects.filter(quiz_instance=self).all()
	
	
class UserResponse(models.Model):
	'''User response to a single question.'''
	quiz_instance = models.ForeignKey(QuizInstance)
	question = models.ForeignKey(MultipleChoice)
	response = models.ManyToManyField(MultipleChoiceAnswer, related_name="response")
	time_taken = models.DateTimeField(_('When was the question posed'), auto_now_add=True)
	time_taken_delta = models.DateTimeField(_('When was the question answered'), blank=True)

	def __unicode__(self):
		return u"Response to %s for %s" % (self.question, self.quiz_instance)
	@property
	def is_correct(self):
		return self.question.correct_answer.all()==self.response.all()

