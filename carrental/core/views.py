from django.core import paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Car, Customer, Store, Transaction


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
        transactions = self.object.transaction_set.filter()
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

class TransactionListView(generic.ListView):
    template_name = "core/transaction_list"
    context_object_name = 'transaction_list'
    paginate_by = 10
    def get_queryset(self):
        """ Returns a list of transactions """
        return Transaction.objects.order_by('id')