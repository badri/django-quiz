'''
view all questions list
1. view question
2. take quiz
3. view quiz response
4. view question response and usage
5. view person details, i.e. how many quizzes they have taken, score
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('quiz.views',
	url(r'^questions/$', 'questions_list'),
	url(r'^question/(?P<id>\d+)/(?P<slug>[-\w]+)/$', 'question'),                       
	url(r'^quiz/(?P<id>\d+)/$', 'quiz'),
)
