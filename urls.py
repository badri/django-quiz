'''
view all questions list
1. view question
2. take quiz
3. view quiz response
4. view question response and usage
5. view person details, i.e. how many quizzes they have taken, score
6. make quiz as AJAX
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('quiz.views',
	url(r'^questions/$', 'questions_list'),
	url(r'^question/(?P<id>\d+)/(?P<slug>[-\w]+)/$', 'question'),                       
        url(r'^quiz/(?P<id>\d+)/take/$', 'create_quiz'),
        url(r'^quiz/(?P<id>\d+)/report/$', 'report'),
        url(r'^quiz/(?P<id>\d+)/result/$', 'result'),
	url(r'^quiz/(?P<id>\d+)/$', 'quiz'),
)
