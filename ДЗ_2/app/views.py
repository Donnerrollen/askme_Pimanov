import copy

from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import HttpResponse, redirect
from django.shortcuts import render
from django import forms
from django.views.decorators.csrf import csrf_exempt
import app.forms as f
# Create your views here.

TAGS = [
    {
        'tag_name': f'black-jack'
    },
    {
        'tag_name': f'bender'
    }
]

ASKS = [
    {
        'text': f'Здесь текст ответа №{i}',
        'is_editable': True if i % 3 == 0 else False,
        'is_correct': True if i % 2 == 0 else False
    } for i in range(1, 21)
]

QUESTIONS = [
    {
        'title': f'Вопрос №{i}',
        'id': i,
        'text': f'Здесь текст вопроса №{i}',
        'tags': TAGS,
        'asks': ASKS
    } for i in range(1, 81)
]

def index(request):
    try:
        page = paginate(QUESTIONS, request, 5)
    except:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')

    return render(
        request, 'index.html',
        context={'questions': page.object_list,
                 'page_obj': page}
    )

def paginate(objects_list, request, per_page=10):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list, per_page)
    page = paginator.page(page_num)
    return page

def hot(request):
    QUESTIONS_DESCR = copy.deepcopy(QUESTIONS)
    QUESTIONS_DESCR.reverse()
    try:
        page = paginate(QUESTIONS_DESCR, request, 5)
    except:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')

    return render(
        request, 'hot.html',
        context={'questions': page.object_list,
                 'page_obj': page}
    )

def tag(request, tag):
    try:
        page = paginate(QUESTIONS, request, 5)
    except:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')

    return render(
        request, 'tag.html',
        context={'questions': page.object_list,
                 'page_obj': page,
                 'tag_name': tag}
    )

def question(request, question_id):
    is_error = False
    error_text = ''

    if request.method == "POST":
        form = f.AnswerForm(request.POST)
        if form.is_valid():
            return redirect('/question/' + str(question_id))
        else:
            if form.data['answer'] == '':
                error_text = 'Sorry, empty answer!'
                is_error = True

    try:
        question = QUESTIONS[question_id-1]
    except:
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')
    page = paginate(question['asks'], request, 4)

    return render(
        request, 'question.html',
        context={'question': question,
                 'question_id': question_id,
                 'asks': page.object_list,
                 'page_obj': page,
                 'error_text': error_text,
                 'is_error': is_error}
    )

def login(request):

    is_error = False
    error_text = ''

    if request.method == "POST":
        form = f.LoginForm(request.POST)
        if form.is_valid():
            return redirect('/')
        else:
            if form.data['password'] == '':
                error_text = 'Sorry, empty password!'
                is_error = True
            if form.data['login'] == '':
                error_text = 'Sorry, empty login!'
                is_error = True
    else:
        form = f.LoginForm()

    return render(
        request, 'login.html',
        context={'form': form,
                 'is_error': is_error,
                 'error_text': error_text}
    )

def signup(request):
    is_error = False
    error_text = ''

    if request.method == "POST":
        form = f.RegisterForm(request.POST)
        if form.data['password'] == '':
            error_text = 'Sorry, empty password!'
            is_error = True
        elif form.data['login'] == '':
            error_text = 'Sorry, empty login!'
            is_error = True
        elif form.data['email'] == '':
            error_text = 'Sorry, empty email!'
            is_error = True
        elif form.data['nickname'] == '':
            error_text = 'Sorry, empty nickname!'
            is_error = True
        elif form.data['password'] != form.data['repeat_password']:
            error_text = 'Passwords don\'t match!'
            is_error = True
        else: return redirect('/')
    form = f.RegisterForm()

    return render(
        request, 'signup.html',
        context={'form': form,
                 'is_error': is_error,
                 'error_text': error_text}
    )

def settings(request):
    is_error = False
    error_text = ''

    return render(
        request, 'settings.html',
        context= {

        }
    )

def ask(request):
    print(request.POST)
    if request.method == "POST":
        if ("submit_1" in request.POST):
            form = f.TitleForm(request.POST)
            title = form.data['title']

            return render(request, 'ask.html',
                    context={
                          'title': title,
                          'is_error_title': False,
                          'error_text_title': "",
                          'is_error_text': False,
                          'error_text_text': "",
                          'is_error_tags': False,
                          'error_text_tags': "",
                    })

        if ("submit_2" in request.POST):
            form = f.AskForm(request.POST)
            title = form.data['title']
            text = form.data['text']
            tags = form.data['tags']
            is_error_title = False
            is_error_text = False
            is_error_tags = False
            error_text_title = ""
            error_text_text = ""
            error_text_tags = ""

            if (title == ""):
                is_error_title = True
                error_text_title = "Sorry, title is empty!"
            if (text == ""):
                is_error_text = True
                error_text_text = "Sorry, text is empty!"
            if (tags == ""):
                is_error_tags = True
                error_text_tags = "Sorry, tags is empty!"

            if (is_error_title == is_error_text == is_error_tags == False):
                return redirect("/")

            return render(request, 'ask.html',
                    context={
                          'title': title,
                          'is_error_title': is_error_title,
                          'error_text_title': error_text_title,
                          'is_error_text': is_error_text,
                          'error_text_text': error_text_text,
                          'is_error_tags': is_error_tags,
                          'error_text_tags': error_text_tags,
                    })
