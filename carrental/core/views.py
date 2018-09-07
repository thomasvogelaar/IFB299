from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Store, Transaction


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