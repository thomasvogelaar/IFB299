from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('stores', login_required(views.StoreListView.as_view()), name='storelist'),
    path('stores/<int:pk>', login_required(views.StoreDetailView.as_view()), name='storedetails'),
    path('cars', views.carlist, name='carlist'),
    path('cars/<int:car_id>', views.cardetails, name='cardetails'),
    path('customers', views.customerlist, name='customerlist'),
    path('customers/<int:customer_id>', views.customerdetails, name='customerdetails'),
    path('transactions', views.transactionlist, name='transactionlist'),
    path('transactions/<int:transaction_id>', views.transactiondetails, name='transactiondetails')
]