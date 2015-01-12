from django.conf.urls import patterns, url

from views import QuestionAddView, HomeView
from views import QuestionEditView
from views import QuestionView
from views import QuizListView
from views import QuizView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quiz.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^quiz$', QuizListView.as_view(), name="quiz_list"),
    url(r'^quiz/(?P<quiz_id>\d+)$', QuizView.as_view(), name="quiz"),
    url(r'^quiz/(?P<quiz_id>\d+)/(?P<question_id>\d+)$', QuestionView.as_view(), name="question"),
    url(r'^quiz/(?P<quiz_id>\d+)/add$', QuestionAddView.as_view(), name="add_question"),
    url(r'^quiz/(?P<quiz_id>\d+)/edit/(?P<question_id>\d+)$', QuestionEditView.as_view(), name="edit_question"),
)