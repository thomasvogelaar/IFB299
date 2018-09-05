from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
    return HttpResponse("Hello, world. You're at the core index.")


@login_required
def storelist(request):
    return HttpResponse("This is the list of stores")