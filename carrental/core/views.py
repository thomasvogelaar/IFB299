from django.core import paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Car, Customer, Store, Transaction
from django import forms
from django.template import Template, Context
from .forms import TransactionsGetForm, CarRecommendForm
from datetime import datetime, timedelta, time


@login_required
def index(request):
    return render(request, 'core/index.html')


class StoreListView(generic.ListView):
    template_name = 'core/store_list.html'
    context_object_name = 'store_list'
    paginate_by = 10
    def get_queryset(self):
        """Returns a list of stores"""
        return Store.objects.order_by('id')


class StoreDetailView(generic.DetailView):
    model = Store
    template_name = 'core/store_details.html'
    transactions_paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(StoreDetailView, self).get_context_data(**kwargs)
        transactions_page = self.request.GET.get("transactions_page")
        transactions = self.object.transaction_set.filter().order_by('-time')
        transactions_paginator = paginator.Paginator(transactions, self.transactions_paginate_by)
        try:
            transactions_page_obj = transactions_paginator.page(transactions_page)
        except:
            transactions_page_obj = transactions_paginator.page(1)
        context["transactions_page_obj"] = transactions_page_obj
        return context


@login_required
def carlist(request):
    return HttpResponse("This is the list of cars")


@login_required
def cardetails(request, car_id):
    return HttpResponse("This is the details page for car id %s." % car_id)

class CarListView(generic.ListView):
    template_name = 'core/car_list.html'
    context_object_name = 'car_list'
    paginate_by = 10
    def get_queryset(self):
        """Returns a list of cars"""
        return Car.objects.order_by('id')


class CarDetailView(generic.DetailView):
    model = Car
    template_name = 'core/car_details.html'
    transactions_paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(CarDetailView, self).get_context_data(**kwargs)
        transactions_page = self.request.GET.get("transactions_page")
        transactions = self.object.transaction_set.filter().order_by('-time')
        transactions_paginator = paginator.Paginator(transactions, self.transactions_paginate_by)
        try:
            transactions_page_obj = transactions_paginator.page(transactions_page)
        except:
            transactions_page_obj = transactions_paginator.page(1)
        context["transactions_page_obj"] = transactions_page_obj
        return context

@login_required
def customerlist(request):
    return HttpResponse("This is the list of customers")


@login_required
def customerdetails(request, customer_id):
    return HttpResponse("This is the details page for customer id %s." % customer_id)


@login_required
def transactionlist(request):
    param = request.GET.get('start_date')
    if param is None:
        form = TransactionsGetForm()
    else:
        form = TransactionsGetForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date'] + timedelta(days=1)
            transactions = Transaction.objects.filter(
                time__gte=start_date
            ).filter(
                time__lte=end_date
            )
            transactions_page = request.GET.get("page")
            print(transactions_page)
            transactions_paginator = paginator.Paginator(transactions, 1)
            try:
                transactions_page_obj = transactions_paginator.page(transactions_page)
            except:
                transactions_page_obj = transactions_paginator.page(1)
            return render(request, 'core/transaction_list.html', {'form': form, 'transaction_list': transactions, 'page_obj': transactions_page_obj, 'paginator': transactions_paginator })
    return render(request, 'core/transaction_list.html', {'form': form })

@login_required
def transactiondetails(request, transaction_id):
    return HttpResponse("This is the details page for transaction id %s." % transaction_id)

class TransactionListView(generic.ListView):
    template_name = "core/transaction_list"
    context_object_name = 'transaction_list'
    paginate_by = 10
    def get_queryset(self):
        """ Returns a list of transactions """
        return Transaction.objects.order_by('id')

class CarRecommendView(generic.TemplateView):
    template_name = "extra/car-recommend.html"
    def get_context_data(self, **kwargs):
        context = super(CarRecommendView, self).get_context_data(**kwargs)
        context["form"] = CarRecommendForm().as_table()
        return context
    
def recommend_car(request: HttpRequest):
    form = CarRecommendForm(request.GET)
    cars = list(Car.cars.all())
    cars = apply_filters(request, cars)
    return render(request, 'extra/car-recommend.html', { 'form': form, 'recommended_cars': cars })

def apply_filters(request: HttpRequest, cars: list):
    if (key_exists(request, "make")):
        cars = filter_cars(cars, "make", request.GET["make"])
    if (key_exists(request, "model")):
        cars = filter_cars(cars, "model", request.GET["model"])
    if (key_exists(request, "series_year")):
        cars = filter_cars(cars, "series_year", request.GET["series_year"])
    if (key_exists(request, "engine_size")):
        cars = filter_cars(cars, "enginesize", request.GET["engine_size"])
    if (key_exists(request, "fuel_system")):
        cars = filter_cars(cars, "fuelsystem", request.GET["fuel_system"])
    if (key_exists(request, "power")):
        cars = filter_cars(cars, "power", request.GET["power"])
    if (key_exists(request, "seats")):
        cars = filter_cars(cars, "seats", request.GET["seats"])
    if (key_exists(request, "body_type")):
        cars = filter_cars(cars, "bodyType", request.GET["body_type"])
    if (key_exists(request, "drive")):
        cars = filter_cars(cars, "drive", request.GET["drive"])
    if (key_exists(request, "wheelbase")):
        cars = filter_cars(cars, "wheelbase", request.GET["wheelbase"])
    return cars

def filter_cars(collection: list, field: str, value: str):
    values = value.split(" ")
    if value.__contains__("<"):
        check_type = "lt"
        values.remove("<")
    elif value.__contains__("BETWEEN"):
        check_type = "between"
        values.remove("BETWEEN")
        values.remove("AND")
    elif value.__contains__(">"):
        check_type = "gt"
        values.remove(">")
    else:
        check_type = "eq"
    
    for item in collection:
        if not check_val(check_type, getattr(item, field), values):
            collection.remove(item)
    return collection

def check_val(check_type: str, value, constraints: list):
    if not constraints[0] or check_type == 'between' and not constraints[1]:
        return True
    elif (check_type == "between"):
        return (int(value) > int(constraints[0]) and int(value) < int(constraints[1]))
    elif (check_type == "lt"):
        return int(value) < int(constraints[0])
    elif (check_type == "gt"):
        return int(value) > int(constraints[0])
    else:
        return str(value) == str(constraints[0])
    


def key_exists(request: HttpRequest, key):
    return key in request.GET
