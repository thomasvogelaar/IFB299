import csv

# script to colate the wanted columns and clean the data 
fieldnames = ['Store_Name', 'Store_Address', 'Store_Phone', 'Store_City', 'Store_State_Name']
removedData = ['Store_ID','Order_ID','Order_CreateDate','Pickup_Or_Return','Pickup_Or_Return_Date',
               'Customer_ID','Customer_Name','Customer_Phone','Customer_Addresss','Customer_Brithday',
               'Customer_Occupation','Customer_Gender','Car_ID','Car_MakeName','Car_Model','Car_Series',
               'Car_SeriesYear','Car_PriceNew','Car_EngineSize','Car_FuelSystem','Car_TankCapacity',
               'Car_Power','Car_SeatingCapacity','Car_StandardTransmission','Car_BodyType','Car_Drive',
               'Car_Wheelbase']
headers = fieldnames + removedData
listLines = []

#open the csv file
with open('dataInStore.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    #open the empty csv file 
    with open('Store.csv', 'w') as new_file:
        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
  
        #delete unwanted lines and write the rest 
        for row in csv_reader:
            for header in headers:
                # remove unwanted data
                if header in removedData:
                    del row[header]
                # shorten row string by 3 if equals to string 'Store_Name' 
                elif header == 'Store_Name':
                    row[header] = row[header][:-6]
            # check for duplicates
            if row in listLines:
                continue
            else:
                csv_writer.writerow(row)
                listLines.append(row)