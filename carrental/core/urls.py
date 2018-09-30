from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('stores', login_required(views.StoreListView.as_view()), name='storelist'),
    path('stores/<int:pk>', login_required(views.StoreDetailView.as_view()), name='storedetails'),
    path('cars', login_required(views.CarListView.as_view()), name='carlist'),
    path('cars/<int:pk>', login_required(views.CarDetailView.as_view()), name='cardetails'),
    path('customers', login_required(views.CustomerListView.as_view()), name='customerlist'),
    path('customers/<int:pk>', login_required(views.CustomerDetailView.as_view()), name='customerdetails'),
    path('transactions', views.transactionlist, name='transactionlist'),
    path('transactions/<int:transaction_id>', views.transactiondetails, name='transactiondetails')
]