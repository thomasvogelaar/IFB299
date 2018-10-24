import csv
import models
import sys
import os
import django

project_dir = "Users\deanm\Desktop\code\repos\django\IFB299\carrental\Data\dataCleaning"

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

django.setup()

from core.models import Store

data = csv.reader(open("/Users/deanm/source/repos/djangoWebsite/carrental/Data/Store.csv"), delimiter = ",")

for row in Store:
    if row[0] != 'create_data':
        Store = Store()
        Store.name = row[0]
        Store.address = row[1]
        Store.phone = row[2]
        Store.city = row[3]
        Store.state = row[4]
        Store.save()

