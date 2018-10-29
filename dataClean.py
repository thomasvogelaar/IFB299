import csv
import sys
import os, imp
import django
import datetime

# script to colate the wanted columns and clean the data 
project_dir = os.path.dirname(__file__)
transaction = 'Customer_Name Car_MakeName Car_Model Car_Series Car_SeriesYear Store_Name Pickup_Or_Return_Date Pickup_Or_Return'
store = ['Store_Name', 'Store_Address', 'Store_Phone', 'Store_City', 'Store_State_Name']
car = ['Car_MakeName','Car_Model','Car_Series', 'Car_SeriesYear','Car_PriceNew','Car_EngineSize','Car_FuelSystem',
       'Car_TankCapacity', 'Car_Power','Car_SeatingCapacity','Car_StandardTransmission','Car_BodyType','Car_Drive', 'Car_Wheelbase']
customer = ['Customer_Name','Customer_Phone','Customer_Addresss','Customer_Brithday', 'Customer_Occupation','Customer_Gender']
headers = ['Store_ID','Store_Name', 'Store_Address', 'Store_Phone', 'Store_City', 'Store_State_Name', 'Order_ID','Order_CreateDate',
               'Pickup_Or_Return','Pickup_Or_Return_Date', 'Customer_ID','Customer_Name','Customer_Phone','Customer_Addresss',
               'Customer_Brithday', 'Customer_Occupation','Customer_Gender','Car_ID','Car_MakeName','Car_Model','Car_Series',
               'Car_SeriesYear','Car_PriceNew','Car_EngineSize','Car_FuelSystem','Car_TankCapacity', 'Car_Power','Car_SeatingCapacity',
               'Car_StandardTransmission','Car_BodyType','Car_Drive', 'Car_Wheelbase']
notStore = [x for x in headers if x not in store]
notCar = [x for x in headers if x not in car]
notCustomer = [x for x in headers if x not in customer]
listLines = []
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()

from core.models import Store
from core.models import Car
from core.models import Customer
from core.models import Transaction

def contains_nulls(row):
    for item in row:
        if item is None or item == 'NULL':
            return True
    return False

#open the csv file
with open('Data/dataCleaning/dataInStore.csv', 'r', encoding="ISO-8859-1") as store_csv_file:
    store_csv_reader = csv.DictReader(store_csv_file)
    with open('Data/dataCleaning/dataInStore.csv', 'r', encoding="ISO-8859-1") as car_csv_file:
        car_csv_reader = csv.DictReader(car_csv_file)
        with open('Data/dataCleaning/dataInStore.csv', 'r', encoding="ISO-8859-1") as customer_csv_file:
            customer_csv_reader = csv.DictReader(customer_csv_file)
            with open('Data/dataCleaning/dataInStore.csv', 'r', encoding="ISO-8859-1") as transaction_csv_file:
                transaction_csv_reader = csv.DictReader(transaction_csv_file)
           
                #open the empty csv file 
                with open('Data/dataCleaning/Store.csv', 'w', encoding="ISO-8859-1") as store_file:
                    store_writer = csv.DictWriter(store_file, fieldnames=store, lineterminator='\n')
                    with open('Data/dataCleaning/Car.csv', 'w', encoding="ISO-8859-1") as car_file:
                        car_writer = csv.DictWriter(car_file, fieldnames=car, lineterminator='\n')
                        with open('Data/dataCleaning/Customer.csv', 'w', encoding="ISO-8859-1") as customer_file:
                            customer_writer = csv.DictWriter(customer_file, fieldnames=customer, lineterminator='\n')    
                            with open('Data/dataCleaning/Transaction.csv', 'w', encoding="ISO-8859-1") as transaction_file:
                                transaction_writer = csv.DictWriter(transaction_file, transaction.split(), extrasaction='ignore', lineterminator='\n')
  
                            #clean and write store csv file
                                for row in store_csv_reader:
                                    for header in headers:
                                        # remove unwanted rows
                                        if header in notStore:
                                            del row[header]
                                        # remove '_store' from all store names 
                                        elif header == 'Store_Name':
                                            row[header] = row[header][:-6]
                                    # check for duplicates
                                    if row in listLines or contains_nulls(row):
                                        continue
                                    else:
                                        store_writer.writerow(row)
                                        listLines.append(row)
                                listLines.clear()
                        
                            #clean and write car csv file
                                for row in car_csv_reader:
                                    for header in headers:
                                        if header in notCar:
                                            del row[header]
                                    if row in listLines or contains_nulls(row):
                                        continue
                                    else:
                                        car_writer.writerow(row)
                                        listLines.append(row)
                                listLines.clear()

                            #clean and write customer csv file
                                for row in customer_csv_reader:
                                    for header in headers:
                                        if header in notCustomer:
                                            del row[header]
                                    if row in listLines or contains_nulls(row):
                                        continue
                                    else:
                                        customer_writer.writerow(row)
                                        listLines.append(row)

                                transaction_writer.writeheader()
             
                                for row in transaction_csv_reader:
                                    for header in headers:
                                        if header == 'Store_Name':
                                            row[header] = row[header][:-6]
                                    transaction_writer.writerow(row)

# import store data
storeData = csv.reader(open("Data/dataCleaning/Store.csv", encoding="ISO-8859-1"), delimiter = ",")
for row in storeData:
    if row[0] != 'create_data' and row[0] is not None and row[0] != 'NULL':
        newstore = Store()
        newstore.name = row[0]
        newstore.address = row[1]
        newstore.phone = row[2]
        newstore.city = row[3]
        newstore.state = row[4]
        newstore.save()

#import car data
carData = csv.reader(open("Data/dataCleaning/Car.csv", encoding="ISO-8859-1"), delimiter = ",")
for row in carData:
    if row[0] != 'create_data' and row[0] is not None and row[0] != 'NULL':
        newcar = Car()
        newcar.make = row[0]
        newcar.model = row[1]
        newcar.series = row[2]
        newcar.series_year = row[3]
        newcar.price = row[4]
        newcar.enginesize = row[5]
        newcar.fuelsystem = row[6]
        newcar.tankcapacity = row[7]
        newcar.power = row[8]
        newcar.seats = row[9]
        newcar.standardtransmission = row[10]
        newcar.bodyType = row[11]
        newcar.drive = row[12]
        newcar.wheelbase = row[13]
        newcar.save()

#import customer data
customerData = csv.reader(open("Data/dataCleaning/Customer.csv", encoding="ISO-8859-1"), delimiter = ",")
for row in customerData:
    if row[0] != 'create_data' and row[0] is not None and row[0] != 'NULL':
        new_customer = Customer()
        new_customer.name = row[0]
        new_customer.phone = row[1]
        new_customer.address = row[2]
        new_customer.birthday = datetime.datetime.strptime(row[3], '%d/%m/%Y').strftime('%Y-%m-%d')
        new_customer.occupation = row[4]
        new_customer.gender = row[5]
        new_customer.save()


transactionData = csv.reader(open("Data/dataCleaning/Transaction.csv", encoding="ISO-8859-1"), delimiter = ",")
# #import transaction data
for row in transactionData:
    if contains_nulls(row):
        continue
    if row[0] != 'Customer_Name' and row[0] is not None and row[0] != 'NULL':
       newtransaction = Transaction()
       newtransaction.customer = Customer.objects.filter(name=row[0])[0]
       newtransaction.car = Car.objects.filter(make=row[1], model=row[2], series=row[3], series_year=row[4])[0]
       newtransaction.store = Store.objects.filter(name=row[5])[0]
       newtransaction.time = datetime.datetime.strptime(row[6], '%Y%m%d').strftime('%Y-%m-%d')
       newtransaction.type = 'PIC' if (row[7] == 'Pickup') else 'RET'
       newtransaction.save()
