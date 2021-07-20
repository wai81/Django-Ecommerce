from django.http import HttpResponse


def home(reqest):
    return HttpResponse('Home page')
