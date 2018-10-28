from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index),
    path('browsecars', views.ExternalCarListView.as_view(), name='externalcarlist'),
    path('cardetails/<int:pk>', views.ExternalCarDetailView.as_view(), name='externalcardetails'),
    path('storedetails/<int:pk>', views.ExternalStoreDetailView.as_view(), name='externalstoredetails'),
    path('stores',
        permission_required("core.view_store")
        (login_required(views.StoreListView.as_view())), name='storelist'),
    path('stores/<int:pk>',
        permission_required("core.view_store")
        (login_required(views.StoreDetailView.as_view())), name='storedetails'),
    path('stores/create',
        permission_required("core.view_store")
        (login_required(views.StoreCreateForm.as_view())), name='storecreateform'),
    path('stores/<int:pk>/edit',
        permission_required("core.view_store")
        (login_required(views.StoreUpdateForm.as_view())), name='storeupdateform'),
    path('cars',
        permission_required("core.view_car")
        (login_required(views.CarListView.as_view())), name='carlist'),
    path('cars/<int:pk>',
        permission_required("core.view_car")
        (login_required(views.CarDetailView.as_view())), name='cardetails'),
    path('cars/create',
        permission_required("Core.view_car")
        (login_required(views.CarCreateForm.as_view())), name='carcreateform'),
    path('cars/<int:pk>/edit',
        permission_required("core.view_car")
        (login_required(views.CarUpdateForm.as_view())), name='carupdateform'),
    path('customers',
        permission_required("core.view_customer")
        (login_required(views.CustomerListView.as_view())), name='customerlist'),
    path('customers/<int:pk>',
        permission_required("core.view_customer")
        (login_required(views.CustomerDetailView.as_view())), name='customerdetails'),
    path('customers/create',
        permission_required("core.view_customer")
        (login_required(views.CustomerCreateForm.as_view())), name='customercreateform'),
    path('customers/<int:pk>/edit',
        permission_required("core.view_customer")
        (login_required(views.CustomerUpdateForm.as_view())), name='customerupdateform'),
    path('transactions', views.transactionlist, name='transactionlist'),
    path('transactions/create', views.TransactionCreateForm.as_view(), name='transactioncreateform'),
    path('recommend-car', views.recommend_car, name="recommendcar"),
]