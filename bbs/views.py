from django.shortcuts import render, redirect

from utils.result_dict_util import ResultDict


def home(request):
    return render(request, "index.html")


def index(request):
    return redirect('/home/')
