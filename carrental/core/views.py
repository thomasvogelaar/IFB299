from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
    return HttpResponse("Hello, world. You're at the core index.")


@login_required
def storelist(request):
    return HttpResponse("This is the list of stores")


@login_required
def storedetails(request, store_id):
    return HttpResponse("This is the details page for store id %s." % store_id)


@login_required
def carlist(request):
    return HttpResponse("This is the list of cars")


@login_required
def cardetails(request, car_id):
    return HttpResponse("This is the details page for car id %s." % car_id)


@login_required
def customerlist(request):
    return HttpResponse("This is the list of customers")


@login_required
def customerdetails(request, customer_id):
    return HttpResponse("This is the details page for customer id %s." % customer_id)


@login_required
def transactionlist(request):
    return HttpResponse("This is the list of transactions")


@login_required
def transactiondetails(request, transaction_id):
    return HttpResponse("This is the details page for transaction id %s." % transaction_id)