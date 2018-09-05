from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stores', views.storelist, name='storelist'),
    path('stores/<int:store_id>', views.storedetails, name='storedetails'),
    path('cars', views.carlist, name='carlist'),
    path('cars/<int:car_id>', views.cardetails, name='cardetails'),
    path('customers', views.customerlist, name='customerlist'),
    path('customers/<int:customer_id>', views.customerdetails, name='customerdetails'),
    path('transactions', views.transactionlist, name='transactionlist'),
    path('transactions/<int:transaction_id>', views.transactiondetails, name='transactiondetails')
]