from django.shortcuts import render


def home(reqest):
    return render(reqest, 'home.html')
