'''
TODO
1. add subjective and true or false questions
2. time per question and time for overall quiz
3. quiz settings
'''

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatewords_html

from quiz.managers import *

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
	answer = models.TextField(_('answer'))

	def __unicode__(self):
		return u"%s" % truncatewords_html(self.answer, 10)

class MultipleChoice(models.Model):
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
	taker = models.ForeignKey(User)
	quiz = models.ForeignKey(Quiz)
	quiz_taken = models.DateTimeField(_('quiz taken'), auto_now_add=True)
	score = models.IntegerField(default=0)
	
	# prevent from setting score in the frontend to avoid tampering
	def __setattr__(self, name, value):
		if name == 'score':
			if getattr(self, 'score', None):
				if getattr(self, 'score') != 0:
					return
		super(QuizInstance, self).__setattr__(name, value)

	
class UserResponse(models.Model):
	quiz_instance = models.OneToOneField(QuizInstance)
	question = models.ForeignKey(MultipleChoice)
	response = models.ManyToManyField(MultipleChoiceAnswer, related_name="response")
	time_taken = models.DateTimeField(_('When was the question posed'))
	time_taken_delta = models.DateTimeField(_('When was the question answered'))

	def is_correct(self):
		return self.question.correct_answer.all()==self.response.all()

