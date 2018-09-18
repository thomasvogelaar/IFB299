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
    path('customers', views.customerlist, name='customerlist'),
    path('customers/<int:customer_id>', views.customerdetails, name='customerdetails'),
    path('transactions', login_required(views.TransactionListView.as_view()), name='transactionlist'),
    path('transactions/<int:transaction_id>', views.transactiondetails, name='transactiondetails'),
    path('car-recommend', views.CarRecommendView.as_view(), name='carrecommend'),
    path('recommend-car', views.recommend_car, name="recommendcar"),
]