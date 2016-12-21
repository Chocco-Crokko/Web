from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import auth
from fl_askapp.models import *
from fl_askapp.forms import *
from fl_askapp import paginator_foo
from django.forms.models import model_to_dict
import random


def index(request, page = '1'):
	myquestions = Question.objects.newest()
	question_list = paginator_foo.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/"
	return render(request, 'index.html', {"questions": question_list}, )

def hot_questions(request, page = '1'):
	myquestions = Question.objects.hot()
	question_list = paginator_foo.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/hot/"
	return render(request, 'hot_questions.html', {"questions": question_list}, )

def profile(request, user_name, page = '1'):
	myquestions = Question.objects.user_questions(user_name)
	profile = Profile.objects.get_by_name(user_name)
	question_list = paginator_foo.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/profile/" + profile[0].user.username + "/"
	return render(request, 'profile.html', {"questions": question_list, "profile": profile[0]}, )

def tag(request, tag, page = '1'):	
	myquestions = Question.objects.tag_search(tag)
	question_list = paginator_foo.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/tag/" + tag + "/"		
	return render(request, 'tag.html', {"questions": question_list, 'tag' : tag}, )

def single_question(request, id, page = '1'):
    question = get_object_or_404(Question, pk=id)
    answers = question.answer_set.all()
    answer_list = paginator_foo.pagination(answers, 4, page)
    answer_list.paginator.baseurl = "/question/id" + id + "/"

    last_page_num = int((answers.count() + 1) / 4 + 1)

    if request.method == "POST":
	    answer_form = AnswerForm(request.POST)
	    if answer_form.is_valid():
		    answer = answer_form.save(question, request.user)
		    return HttpResponseRedirect(reverse('question', kwargs={'id': question.id, 'page' : last_page_num})
									    + '#answer_' + str(answer.id))
    else:
	    answer_form = AnswerForm()
    return render(request, 'question.html', {"question": question, "answers" : answer_list, "new_question" : True, "form" : answer_form},)

def developing(request):
	return render(request, 'developing.html', {},)

@login_required
def ask_question(request):
	if request.method == "POST":
		form = QuestionForm(request.POST)
		if form.is_valid():
			q = form.save(request.user, 0)
			return HttpResponseRedirect(reverse('question', kwargs={'id': q.id}))
	else:
		form = QuestionForm()
	return render(request, 'ask.html', {'form': form},)

@login_required
def edit_question(request, id):
	question = get_object_or_404(Question, pk=id)
	if question.user != request.user:
		return HttpResponseRedirect(reverse('question', kwargs={'id': id}))
	if request.method == "POST":
		form = QuestionForm(request.POST)
		if form.is_valid():
			q = form.save(request.user, id)
			return HttpResponseRedirect(reverse('question', kwargs={'id': q.id}))
	else:
		q = model_to_dict(question)
		tags = question.tags.all()
		q['tags'] = ''
		first = True
		for tag in tags:
			if first:
				q['tags'] = tag.text
				first = False
			else:
				q['tags'] = q['tags'] + ',' + tag.text
		form = QuestionForm(q)
	return render(request, 'ask.html', {'form': form}, )

def login(request):
	redirect = request.GET.get('continue', '/')

	if request.user.is_authenticated():
		return HttpResponseRedirect(redirect)

	if request.method == "POST":
		form = LoginForm(request.POST)

		if form.is_valid():
			auth.login(request, form.cleaned_data['user'])
			return HttpResponseRedirect(redirect)
	else:
		form = LoginForm()
	return render(request, 'login.html', {'form': form},)

@login_required
def logout(request):
	redirect = request.GET.get('continue', '/')
	auth.logout(request)
	return HttpResponseRedirect(redirect)

def signup(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')

	if request.method == "POST":
		form = SignupForm(request.POST, request.FILES)
		if form.is_valid():
			user = form.save()
			auth.login(request, user)
			return HttpResponseRedirect('/')
	else:
		form = SignupForm()

	return render(request, 'signup.html', {'form': form},)

@login_required
def profile_edit(request):
	if request.method == "POST":
		form = ProfileEditForm(request.POST, request.FILES)

		if form.is_valid():
			form.save(request.user)
			form.status = True
			#return HttpResponseRedirect('/profile/' + request.user.username + '/')
	else:
		u = model_to_dict(request.user)
		up = request.user.profile
		u['information'] = up.information
		form = ProfileEditForm(u)
		form.status = False
	return render(request, 'edit_profile.html', {'form': form},)

@login_required
def change_password(request):
	if request.method == "POST":
		form = ChangePasswordForm(request.POST)
		form.user = request.user
		if form.is_valid():
			form.save(request.user)
			form.status = True
			#return HttpResponseRedirect('/')
	else:
		form = ChangePasswordForm()
		form.user = request.user
	return render(request, 'change_password.html', {'form': form}, )

@csrf_exempt
def get_prms(request):
    response = "<p> GET/POST </p>" \
               "<form method='POST'>"\
               "<p><input type='text' name='text'></p>" \
               "<p><input type='submit' value='Send!'></p>" \
               "</form>"
    if request.method == 'GET':
        if request.GET:
            response += "<h3> <p> Get data: </p> </h3>"
            for key,value in request.GET.iteritems():
                if len(value) == 1:
                    response += "%s = %s <br>" % (key, value[0])
                else:
                    response += "%s = %s <br>" % (key, value)
    elif request.method == 'POST':
        response += "<h3> <p> Post data: </p> </h3>"
        response += "Value = %s <br>" % (request.POST.get('text'))
    return HttpResponse(response, content_type="text/html", status=200)
