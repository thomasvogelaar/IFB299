from django.core import paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Car, Customer, Store, Transaction
from .forms import TransactionsGetForm
from datetime import datetime, timedelta, time
from graphos.sources.model import ModelDataSource
from graphos.renderers import gchart


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
            transactions_per_page = 10
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date'] + timedelta(days=1)
            transactions = Transaction.objects.filter(
                time__gte=start_date
            ).filter(
                time__lte=end_date
            )
            # FIXME do
            transaction_data = Transaction.objects.all()
            data_source = ModelDataSource(transaction_data, fields=['time'])
            chart = gchart.LineChart(data_source)
            transactions_page = request.GET.get("page")
            transactions_paginator = paginator.Paginator(transactions, transactions_per_page)
            try:
                transactions_page_obj = transactions_paginator.page(transactions_page)
            except:
                transactions_page_obj = transactions_paginator.page(1)
            return render(request, 'core/transaction_list.html', {'form': form, 'transaction_list': transactions, 'page_obj': transactions_page_obj, 'paginator': transactions_paginator, 'chart': chart })
    return render(request, 'core/transaction_list.html', {'form': form })


@login_required
def transactiondetails(request, transaction_id):
    return HttpResponse("This is the details page for transaction id %s." % transaction_id)