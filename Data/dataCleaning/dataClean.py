import csv
import sys
import os
import django

# script to colate the wanted columns and clean the data 
project_dir = "Users\deanm\Desktop\code\repos\django\IFB299\carrental\Data\dataCleaning"
storeData = csv.reader(open("/Users/deanm/Desktop/code/repos/django/IFB299/carrental/Data/dataCleaning/Store.csv"), delimiter = ",")
carData = csv.reader(open("/Users/deanm/Desktop/code/repos/django/IFB299/carrental/Data/dataCleaning/Car.csv"), delimiter = ",")
customerData = csv.reader(open("/Users/deanm/Desktop/code/repos/django/IFB299/carrental/Data/dataCleaning/Customer.csv"), delimiter = ",")
transactionData = csv.reader(open("/Users/deanm/Desktop/code/repos/django/IFB299/carrental/Data/dataCleaning/Transaction.csv"), delimiter = ",")
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

#open the csv file
with open('dataInStore.csv', 'r') as store_csv_file:
    store_csv_reader = csv.DictReader(store_csv_file)
    with open('dataInStore.csv', 'r') as car_csv_file:
        car_csv_reader = csv.DictReader(car_csv_file)
        with open('dataInStore.csv', 'r') as customer_csv_file:
            customer_csv_reader = csv.DictReader(customer_csv_file)
            with open('dataInStore.csv', 'r') as transaction_csv_file:
                transaction_csv_reader = csv.DictReader(transaction_csv_file)
           
                #open the empty csv file 
                with open('Store.csv', 'w') as store_file:
                    store_writer = csv.DictWriter(store_file, fieldnames=store)
                    with open('Car.csv', 'w') as car_file:
                        car_writer = csv.DictWriter(car_file, fieldnames=car)
                        with open('Customer.csv', 'w') as customer_file:
                            customer_writer = csv.DictWriter(customer_file, fieldnames=customer)    
                            with open('Transaction.csv', 'w') as transaction_file:
                                transaction_writer = csv.DictWriter(transaction_file, transaction.split(), extrasaction='ignore')
  
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
                                    if row in listLines:
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
                                    if row in listLines:
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
                                    if row in listLines:
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
                                for row in storeData:
                                    if row[0] != 'create_data':
                                        Store = Store()
                                        Store.name = row[0]
                                        Store.address = row[1]
                                        Store.phone = row[2]
                                        Store.city = row[3]
                                        Store.state = row[4]
                                        Store.save()

                                #import car data
                                for row in carData:
                                    if row[0] != 'create_data':
                                        Car = Car()
                                        Car.make = row[0]
                                        Car.model = row[1]
                                        Car.series = row[2]
                                        Car.series_year = row[3]
                                        Car.price = row[4]
                                        Car.enginesize = row[5]
                                        Car.fuelsystem = row[6]
                                        Car.tankcapacity = row[7]
                                        Car.power = row[8]
                                        Car.seats = row[9]
                                        Car.standardtransmission = row[10]
                                        Car.bodyType = row[11]
                                        Car.drive = row[12]
                                        Car.wheelbase = row[13]
                                        Car.save()

                                #import customer data
                                for row in customerData:
                                    if row[0] != 'create_data':
                                       Customer = Customer()
                                       Customer.name = row[0]
                                       Customer.phone = row[1]
                                       Customer.address = row[2]
                                       Customer.birthday = row[3]
                                       Customer.occupation = row[4]
                                       Customer.gender = row[5]
                                       Customer.save()


                                #import transaction data
                                for row in transactionData:
                                    car = row[2]+row[3]+row[4]+row[5]
                                    if row[0] != 'create_data':
                                       Transaction = Transaction()
                                       Transaction.customer = row[0]
                                       Transaction.car = row[4]
                                       Transaction.store = car
                                       Transaction.time = row[6]
                                       Transaction.type = row[7]
                                       Transaction.save()