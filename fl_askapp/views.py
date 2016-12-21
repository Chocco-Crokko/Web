from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from fl_askapp.models import *
from fl_askapp import paginator_foo
import random


def index(request, page = '1'):
	user = { "user_is_logged" : False}	
	myquestions = Question.objects.newest()
	question_list = paginator_foo.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/"
	return render(request, 'index.html', {"questions": question_list, "user" : user}, )

def hot_questions(request, page = '1'):
	user = { "user_is_logged" : True}
	myquestions = Question.objects.hot()
	question_list = paginator_foo.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/hot/"
	return render(request, 'hot_questions.html', {"questions": question_list, "user" : user}, )

def profile(request, user_name, page = '1'):
	user = {"user_is_logged": True}
	myquestions = Question.objects.user_questions(user_name)
	profile = Profile.objects.get_by_name(user_name)
	question_list = paginator_foo.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/profile/" + profile[0].user.username + "/"
	return render(request, 'profile.html', {"questions": question_list, "profile": profile[0], "user" : user}, )

def tag(request, tag, page = '1'):	
	user = { "user_is_logged" : True}
	myquestions = Question.objects.tag_search(tag)
	question_list = paginator_foo.pagination(myquestions, 5, page)
	question_list.paginator.baseurl = "/tag/" + tag + "/"		
	return render(request, 'tag.html', {"questions": question_list, "user" : user, "tag" : tag}, )

def single_question(request, id, page = '1'):
	user = { "user_is_logged" : True}	
	question = Question.objects.get(pk=id)
	answers = question.answer_set.all()
	answer_list = paginator_foo.pagination(answers, 4, page)
	answer_list.paginator.baseurl = "/question/id" + id + "/"
	return render(request, 'question.html', {"question": question, "answers" : answer_list, "user" : user},)

def developing(request):
	user = { "user_is_logged" : True}	
	return render(request, 'developing.html', {"user" : user},)

def ask_question(request):
	user = { "user_is_logged" : True}	
	return render(request, 'ask.html', {"user" : user},)

def login(request):
	user = { "user_is_logged" : False}
	return render(request, 'login.html', {"user" : user},)

def signup(request):
	user = { "user_is_logged" : False}
	return render(request, 'signup.html', {"user" : user},)

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
