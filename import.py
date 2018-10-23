import csv
import models
import sys
import os
import django

project_dir = "../carrental/"

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

django.setup()

from core.models import Store

data = csv.reader(open("./Data/Store.csv"), delimiter = ",")

for row in Store:
    if row[0] != 'create_data':
        Store = Store()
        Store.name = row[0]
        Store.address = row[1]
        Store.phone = row[2]
        Store.city = row[3]
        Store.state = row[4]
        Store.save()

