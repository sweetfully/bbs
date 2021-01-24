from django.shortcuts import render

from utils.result_dict_util import ResultDict


def home(request):
    return render(request, "index.html")