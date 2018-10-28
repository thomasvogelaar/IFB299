from django.test import TestCase
from django.http import HttpRequest
from . import models
from . import helpers
from . import forms
from . import views
import datetime

# Create your tests here.


class CarTestCase(TestCase):    
  def setUp(self):
    models.Car.objects.create(make = 'BMW', model = '1', series_year = '1999', fuelsystem = '123', power = 'AAA', seats = 5, bodyType = 'Yes', drive = '4W', wheelbase = '2577', price = 0)

  def test_car_recommend(self):
    request = HttpRequest()
    request.GET.update({ 'make': 'bmw', 'model': '1', 'series_year': '1999', 'fuelsystem': '123', 'power': 'AAA', 'seats': '5', 'bodyType': 'Yes', 'drive': '4W', 'car_size': 'BETWEEN 2553 AND 2877 ' })
    
    expected_cars = [models.Car.objects.get(make = 'BMW')]
    filtered_cars = helpers.recommend.apply_filters(request, models.Car.objects.all())
    self.assertEqual(filtered_cars, expected_cars, 'Car recommend result not as expected')

class DateSelectTest(TestCase):
  def setUp(self):
    now = datetime.datetime.now()
    test_car = models.Car.objects.create(make = 'BMW', model = '1', series_year = '1999', fuelsystem = '123', power = 'AAA', seats = 5, bodyType = 'Yes', drive = '4W', wheelbase = '2577', price = 0)
    test_store = models.Store.objects.create(name = 'Test Store', address = 'Fake St', phone = '0486907542', city = 'Yes', state = models.State.QLD.name)
    test_customer = models.Customer.objects.create(name = 'John', address = 'Fake St', phone = '0486907542', birthday = now, occupation = models.Occupation.LAB, gender = models.Gender.MA)

    models.Transaction.objects.create(customer = test_customer, store = test_store, car = test_car, time = now, type = models.TransactionType.RET.name)
    models.Transaction.objects.create(customer = test_customer, store = test_store, car = test_car, time = now - datetime.timedelta(days = 1), type = models.TransactionType.PIC.name)
    models.Transaction.objects.create(customer = test_customer, store = test_store, car = test_car, time = now + datetime.timedelta(days = 1), type = models.TransactionType.PIC.name)
    models.Transaction.objects.create(customer = test_customer, store = test_store, car = test_car, time = now + datetime.timedelta(days = 1), type = models.TransactionType.PIC.name)
    models.Transaction.objects.create(customer = test_customer, store = test_store, car = test_car, time = now + datetime.timedelta(days = 1), type = models.TransactionType.PIC.name)
    models.Transaction.objects.create(customer = test_customer, store = test_store, car = test_car, time = now + datetime.timedelta(minutes = 30), type = models.TransactionType.PIC.name)

  def test_date_select(self):
    now = datetime.datetime.now()
    start_date = now
    end_date = now + datetime.timedelta(days = 2)

    result = helpers.transactions.get_transactions_by_dates(start_date, end_date)
    result_count = 0
    for transaction in result:
      result_count += 1
    self.assertEqual(result_count, 4, 'Transaction date select result not as expected')

  def test_date_range(self):
    now = datetime.datetime.now()
    start_date = now
    end_date = now + datetime.timedelta(days = 2)
    range = helpers.transactions.create_daterange(start_date, end_date)
    range_count = 0
    for day in range:
      range_count += 1
    self.assertEqual(range_count, 2, 'Date range result not as expected')

  def test_day_sort(self):
    now = datetime.datetime.now()
    start_date = now
    end_date = now + datetime.timedelta(days = 2)
    range = helpers.transactions.create_daterange(start_date, end_date)
    result = helpers.transactions.sort_by_day(models.Transaction.objects.all(), range)
    self.assertEqual(result[1][2], 1, 'Day sort result not as expected')
    self.assertEqual(result[2][1], 5, 'Day sort result not as expected')


  def test_type_sort(self):
    result = helpers.transactions.split_by_type(models.Transaction.objects.all())
    self.assertEqual(result[1][1], 5)
    self.assertEqual(result[2][1], 1)

