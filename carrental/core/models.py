from django.db import models
from enum import Enum


# List of all possible states
class State(Enum):
    QLD = "Queensland"
    NSW = "New South Wales"
    VIC = "Victoria"
    ACT = "Australian Capital Territory"
    TAS = "Tasmania"
    NT = "Northern Territory"
    SA = "South Australia"
    WA = "Western Australia"


# List of all possible occupations
class Occupation(Enum):
    LAB = "Labour"
    MAN = "Manager"
    RET = "Retiree"
    NUR = "Nurse"
    RES = "Researcher"
    OTH = "Other"


# List of all possible genders
class Gender(Enum):
    MA = "Male"
    FE = "Female"


# List of all possible transaction types
class TransactionType(Enum):
    PIC = "Pickup"
    RET = "Return"


# Represents a store in the system
class Store(models.Model):
    name = models.CharField(max_length = 50)
    address = models.CharField(max_length = 200)
    phone = models.CharField(max_length = 30)
    city = models.CharField(max_length = 200)
    state = models.CharField(
        max_length = 40,
        choices = [(item.name, item.value) for item in State]
    )
    def __str__(self):
        return self.name


# Represents a car in the system
class Car(models.Model):
    make = models.CharField(max_length = 100)
    model = models.CharField(max_length = 100)
    series = models.CharField(max_length = 100)
    series_year = models.CharField(max_length = 100)
    price = models.IntegerField()
    enginesize = models.CharField(max_length = 10)
    fuelsystem = models.CharField(max_length = 100)
    tankcapacity = models.CharField(max_length = 100)
    power = models.CharField(max_length = 10)
    seats = models.IntegerField()
    standardtransmission = models.CharField(max_length = 100)
    bodyType = models.CharField(max_length = 100)
    drive = models.CharField(max_length = 50)
    wheelbase = models.CharField(max_length = 20)
    def __str__(self):
        return self.name + ' ' + self.model + ' ' + self.series + ' ' + ' (' + self.series_year + ')'


# Represents a customer in the system
class Customer(models.Model):
    name = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 30)
    address = models.CharField(max_length = 200)
    birthday = models.DateField()
    occupation = models.CharField(
        max_length = 20,
        choices = [(item.name, item.value) for item in Occupation]
    )
    gender = models.CharField(
        max_length = 10,
        choices = [(item.name, item.value) for item in Gender]
    )
    def __str__(self):
        return self.name


# Represents a transaction within the system
class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    car = models.ForeignKey(Car, on_delete = models.CASCADE)
    store = models.ForeignKey(Store, on_delete = models.CASCADE)
    time = models.DateTimeField()
    type = models.CharField(
        max_length = 10,
        choices = [(item.name, item.value) for item in TransactionType],
        default = "Pickup"
    )
    def __str__(self):
        return 'Transaction ID' + self.ID
