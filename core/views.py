from django.core import paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Car, Customer, Store, Transaction
from django import forms
from django.template import Template, Context
from .forms import TransactionsGetForm, CarRecommendForm, ExternalStoreSelectForm
from .helpers.recommend import apply_filters
from datetime import datetime, timedelta, time
from .helpers.transactions import create_chart, get_transactions_by_dates
from bootstrap_datepicker_plus import DatePickerInput


def index(request):
    """ Renders the main screen template. """
    return render(request, 'core/index.html')


class StoreListView(generic.ListView):
    """ Represents the car list view. Extends the generic list view class. """
    template_name = 'core/store_list.html'
    context_object_name = 'store_list'
    paginate_by = 10
    def get_queryset(self):
        """Returns a list of stores"""
        return Store.objects.order_by('id')


class StoreDetailView(generic.DetailView):
    """ Represents the store detail view. Extends the generic detail view class. """
    model = Store
    template_name = 'core/store_details.html'
    transactions_paginate_by = 10
    def get_context_data(self, **kwargs):
        """Povides the data (in the form of a context object) for the store details page."""
        context = super(StoreDetailView, self).get_context_data(**kwargs)
        transactions_page = self.request.GET.get("transactions_page")
        transactions = self.object.transaction_set.filter().order_by('-time')
        transactions_paginator = paginator.Paginator(transactions, self.transactions_paginate_by)
        try:
            transactions_page_obj = transactions_paginator.page(transactions_page)
        except:
            transactions_page_obj = transactions_paginator.page(1)
        context["transactions_page_obj"] = transactions_page_obj
        context["transactions_paginator"] = transactions_paginator
        return context


class ExternalCarListView(generic.ListView):
    """ Represents the external car list view. Extends the generic list view class. """
    template_name = 'core/external_car_list.html'
    context_object_name = 'car_list'
    paginate_by = 10


class ExternalCarDetailView(generic.DetailView):
    """ Represents the external car details view. Extends the generic details view class. """
    model = Car
    template_name = 'core/external_car_details.html'


class ExternalStoreDetailView(generic.DetailView):
    """ Represents the external store details view. Extends the generic details view class. """
    model = Store
    template_name = 'core/external_store_details.html'
    def get_context_data(self, **kwargs):
        context = super(ExternalStoreDetailView, self).get_context_data(**kwargs)
        print(context)
        form = ExternalStoreSelectForm(initial={'store': context['store'].id})
        context['form'] = form
        return context

    def get(self, request, *args, **kwargs):
        if (request.GET.get('store') is not None):
            return HttpResponseRedirect(request.GET.get('store'))
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class CarListView(generic.ListView):
    """ Represents the car list view. Extends the generic list view class. """
    template_name = 'core/car_list.html'
    context_object_name = 'car_list'
    paginate_by = 10
    def get_queryset(self):
        """Returns a list of cars"""
        return Car.objects.order_by('id')


class CarDetailView(generic.DetailView):
    """ Represents the car detail view. Extends the generic detail view class. """
    model = Car
    template_name = 'core/car_details.html'
    transactions_paginate_by = 10
    def get_context_data(self, **kwargs):
        """Provides the data (in the form of a context object) for the car details page."""
        context = super(CarDetailView, self).get_context_data(**kwargs)
        transactions_page = self.request.GET.get("transactions_page")
        transactions = self.object.transaction_set.filter().order_by('-time')
        transactions_paginator = paginator.Paginator(transactions, self.transactions_paginate_by)
        try:
            transactions_page_obj = transactions_paginator.page(transactions_page)
        except:
            transactions_page_obj = transactions_paginator.page(1)
        context["transactions_page_obj"] = transactions_page_obj
        context["transactions_paginator"] = transactions_paginator
        return context


class CustomerListView(generic.ListView):
    """  Represents the customer list view. Extends the generic list view class. """
    template_name = 'core/customer_list.html'
    context_object_name = 'customer_list'
    paginate_by = 10
    def get_queryset(self):
        """Returns a list of customers"""
        return Customer.objects.order_by('id')


class CustomerDetailView(generic.DetailView):
    """ Represents the customer detail view. Extends the generic detail view class. """
    model = Customer
    template_name = 'core/customer_details.html'
    transactions_paginate_by = 10
    def get_context_data(self, **kwargs):
        """Provides the data (in the form of a context object) for the customer details page."""
        context = super(CustomerDetailView, self).get_context_data(**kwargs)
        transactions_page = self.request.GET.get("transactions_page")
        transactions = self.object.transaction_set.filter().order_by('-time')
        transactions_paginator = paginator.Paginator(transactions, self.transactions_paginate_by)
        try:
            transactions_page_obj = transactions_paginator.page(transactions_page)
        except:
            transactions_page_obj = transactions_paginator.page(1)
        context["transactions_page_obj"] = transactions_page_obj
        context["transactions_paginator"] = transactions_paginator
        return context


class CustomerCreateForm(generic.edit.CreateView):
    """ Represents the customer create form view. """
    # The Generic CreateView class automatically searches for template core/customer_form
    model = Customer
    fields = ['name', 'phone', 'address', 'birthday', 'occupation', 'gender']
    success_url = '/customers?createsuccess=true'

    def get_form(self, form_class=None):
        """ Extending the generic createview get_form function to change the birthday form field widget. """
        if form_class is None: form_class = self.get_form_class()
        form = super(CustomerCreateForm, self).get_form(form_class)
        form.fields['birthday'].widget = DatePickerInput()
        return form


class CustomerUpdateForm(generic.edit.UpdateView):
    """ Represents the customer update form view. """
    # The Generic UpdateView class automatically searches for template core/customer_form
    model = Customer
    fields = ['name', 'phone', 'address', 'birthday', 'occupation', 'gender']
    success_url = '/customers?updatesuccess=true'

    def get_form(self, form_class=None):
        """ Extending the generic updateview get_form function to change the birthday form field widget. """
        if form_class is None: form_class = self.get_form_class()
        form = super(CustomerUpdateForm, self).get_form(form_class)
        form.fields['birthday'].widget = DatePickerInput()
        return form


@login_required
@permission_required("core.view_transaction")
def transactionlist(request):
    """
    Generates the data required for the transactions list view.
    Most of the logic behind this is in the helper functions in ./helpers/transactions.py
    """
    transactions_per_page = 10
    context = {}
    if request.GET.get('start_date') is None:
        form = TransactionsGetForm()
        context = {'form': form }
    else:
        form = TransactionsGetForm(request.GET)
        context = {'form': form }
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date'] + timedelta(days=1)
            transactions = get_transactions_by_dates(start_date, end_date)

            chart = {}
            if form.cleaned_data['media_type'] == 'line':
                chart = create_chart(transactions, start_date, end_date, 'line')
            elif form.cleaned_data['media_type'] == 'pie':
                chart = create_chart(transactions, start_date, end_date, 'pie')
            elif form.cleaned_data['media_type'] == 'bar':
                chart = create_chart(transactions, start_date, end_date, 'bar')
            else:
                chart = {}
            transactions_paginator = paginator.Paginator(transactions, transactions_per_page)
            try:
                transactions_page_obj = transactions_paginator.page(request.GET.get("page"))
            except:
                transactions_page_obj = transactions_paginator.page(1)
            context = {
                'form': form,
                'transaction_list': transactions,
                'page_obj': transactions_page_obj,
                'paginator': transactions_paginator,
                'chart': chart,
                'media_type': form.cleaned_data['media_type']
                }
    return render(request, 'core/transaction_list.html', context)


def recommend_car(request: HttpRequest):
    """ Renders the recommend car form. """
    form = CarRecommendForm(request.GET)
    cars = list(Car.objects.all())
    cars = apply_filters(request, cars)
    if (len(list(request.GET.values())) == 0):
        return render(request, 'extra/car-recommend.html', { 'form': form })    
    return render(request, 'extra/car-recommend.html', { 'form': form, 'recommended_cars': cars })
