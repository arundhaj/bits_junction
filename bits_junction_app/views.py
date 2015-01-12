import random, string

from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail.message import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import generic

from forms import QuestionForm, OptionInlineFormSet
from models import Quiz, Question, Option

class HomeView(generic.View):
    def get(self, request):
        context = RequestContext(request, {})
        return render_to_response('fb_home.html', context)
    
class SignInAndSignUp(generic.View):
    def get(self, request):
        context = RequestContext(request, {})
        
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('quiz_list'))
        else:
            return render_to_response('index.html', context)
        
class SignUp(generic.View):
    def get(self, request):
        
        if 'signup' in request.path:
            step = 'signup'
        else:
            step = 'reset'
            
        context = RequestContext(request, {
            'step': step,
        })
        
        return render_to_response('create_user.html', context)

    def post(self, request):
        action = request.POST.get("step", "")
        username = request.POST.get("bitsID", "").lower()
        
        if action == 'signup':
            firstname = request.POST.get("firstname", "")
            lastname = request.POST.get("lastname", "")
            email = username + '@wilp.bits-pilani.ac.in'
            password = ''.join(random.sample(string.uppercase + string.lowercase + string.digits, 6))
            
            try:
                usr = User.objects.get(username=username)
            except ObjectDoesNotExist:
                usr = None
                
            if usr == None:
                usr = User.objects.create_user(username, email, password)
                usr.first_name = firstname
                usr.last_name = lastname
                usr.save()

                # send mail
                send_mail(email, username, password)
                
                response_text = 'Successfully registered the user. An auto generated password has been set to %s.' % email
            else: 
                response_text = 'User already exists.'
        elif action == 'reset':
            email = username + '@wilp.bits-pilani.ac.in'

            try:
                usr = User.objects.get(username=username)
            except ObjectDoesNotExist:
                usr = None
            
            if usr != None:
                password = ''.join(random.sample(string.uppercase + string.lowercase + string.digits, 6))
                usr.set_password(password)
                usr.save()
                
                # send mail
                send_mail(email, username, password)
            
                response_text = 'Successfully reset password. An auto generated password has been set to %s.' % email
            else:
                response_text = 'Please sign up.'
        
        context = RequestContext(request, {
            'step': 'message',
            'response_text': response_text,
        })
        
        return render_to_response('create_user.html', context)
    
def send_mail(to_email, username, password):
        subject, from_email = 'Login details from BITS Junction', 'arundhaj@arundhaj.com'
        html_content = render_to_string('email.html', {
                                'username': username,
                                'password': password,
                           })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class Authenticate(generic.View):
    def post(self, request):
        username = request.POST.get("bitsID", "").lower()
        password = request.POST.get("password", "")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/quiz")
        else:
            return HttpResponseRedirect(reverse('login'))
#             return HttpResponseRedirect(reverse('quiz_list', args=(year,)))

class LogoutView(generic.RedirectView):
    def get(self, request):
        auth.logout(request)
        
        return HttpResponseRedirect(reverse('login'))

class QuizListViewRedirect(generic.View):
    def get(self, request):
        return HttpResponseRedirect(reverse('quiz_list'))

class QuizListView(generic.View):
    def get(self, request):
        quiz_list = Quiz.objects.all()

        context = RequestContext(request, {
            'quiz_list': quiz_list,
        })
        
        return render_to_response('quiz_list.html', context)

class VideoView(generic.View):
    def get(self, request):
        video_url = "https://www.youtube.com/watch?v=L2kPKn_DGsg"

        context = RequestContext(request, {
            'video_url': video_url,
        })

        return render_to_response('video.html', context)

class QuizView(generic.View):
    def get(self, request, quiz_id=''):
#         question_list = Question.objects.all()
        quiz = Quiz.objects.get(id=quiz_id)
        question_list = Question.objects.filter(quiz_id=quiz_id)

        context = RequestContext(request, {
            'quiz': quiz,
            'question_list': question_list
        })
        
        return render_to_response('quiz.html', context)

class QuestionView(generic.View):
    def get(self, request, quiz_id='', question_id=''):
        quiz = Quiz.objects.get(id=quiz_id)
        question = Question.objects.get(id=question_id)
        option_list = Option.objects.filter(question_id=question_id)
        
        try:
            next_question = question.get_next_by_creation_date(quiz_id=quiz_id)
        except ObjectDoesNotExist:
            next_question = None
            
        try:
            prev_question = question.get_previous_by_creation_date(quiz_id=quiz_id)
        except ObjectDoesNotExist:
            prev_question = None
            
        context = RequestContext(request, {
            'quiz': quiz,
            'question': question,
            'option_list': option_list,
            'prev_question': prev_question,
            'next_question': next_question
        })
            
        return render_to_response('question.html', context)
        
class QuestionAddView(generic.View):
    def get(self, request, quiz_id=''):
        quiz = Quiz.objects.get(id=quiz_id)
        
        question_form = QuestionForm(initial={'quiz': quiz_id, 'type': 'SC'})
        question_formset = OptionInlineFormSet()
        
        context = RequestContext(request, {
            'action_url': '/quiz/%s/add' % quiz_id,
            'quiz': quiz,
            'question_form': question_form,
            'option_list': question_formset,
        })

        return render_to_response('question_edit.html', context)
    
    def post(self, request, quiz_id=''):
        question_form = QuestionForm(data=request.POST)

        if question_form.is_valid():
            question = question_form.save()

            question_formset = OptionInlineFormSet(request.POST, request.FILES, instance=question)
            
            if question_formset.is_valid():
                question_formset.save()

        return redirect("/quiz/%s" % quiz_id)

class QuestionEditView(generic.View):
    def get(self, request, quiz_id='', question_id=''):
        quiz = Quiz.objects.get(id=quiz_id)
        question = Question.objects.get(id=question_id)
        
        question_form = QuestionForm(instance=question)
        question_formset = OptionInlineFormSet(instance=question, queryset=Option.objects.order_by('order'))
            
        context = RequestContext(request, {
            'action_url': '/quiz/%s/edit/%s' % (quiz_id, question_id),
            'quiz': quiz,
            'question': question,
            'option_list': question_formset,
            'question_form': question_form,
        })

        return render_to_response('question_edit.html', context)
    
    def post(self, request, quiz_id='', question_id=''):
        question = Question.objects.get(id=question_id)

        question_form = QuestionForm(data=request.POST, instance=question)
            
        if question_form.is_valid():
            question = question_form.save()
            question_formset = OptionInlineFormSet(request.POST, request.FILES, instance=question)
            
            if question_formset.is_valid():
                question_formset.save()

        return redirect("/quiz/%s/%s" % (quiz_id, question_id))
