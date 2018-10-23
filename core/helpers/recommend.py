from django.http import HttpRequest
import datetime

# Filters the car list by request parameters
def apply_filters(request: HttpRequest, cars: list):
    cars = filter_cars(cars, "make", request.GET.get("make"))
    cars = filter_cars(cars, "model", request.GET.get("model"))
    cars = filter_cars(cars, "series_year", request.GET.get("car_age"))
    cars = filter_cars(cars, "enginesize", request.GET.get("engine_size"))
    cars = filter_cars(cars, "fuelsystem", request.GET.get("fuel_system"))
    cars = filter_cars(cars, "power", request.GET.get("power"))
    cars = filter_cars(cars, "seats", request.GET.get("seats"))
    cars = filter_cars(cars, "bodyType", request.GET.get("body_type"))
    cars = filter_cars(cars, "drive", request.GET.get("drive"))
    cars = filter_cars(cars, "wheelbase", request.GET.get("wheelbase"))
    return cars

def filter_cars(collection: list, field: str, value: str):
    isAge = bool(field == "series_year")
    if (value == '' or value is None):
        return collection
    values = value.split(" ")
    if value.__contains__("<"):
        check_type = "lt"
        values.remove("<")
    elif value.__contains__("BETWEEN"):
        check_type = "between"
        values.remove("BETWEEN")
        values.remove("AND")
    elif value.__contains__(">"):
        check_type = "gt"
        values.remove(">")
    else:
        check_type = "eq"
    
    for item in collection:
        if not check_val(check_type, getattr(item, field), values, isAge):
            collection.remove(item)
    return collection

def check_val(check_type: str, value, constraints: list, isAge: bool):
    if isAge:
        value = datetime.datetime.now().year - int(value)
    if not constraints[0] or (check_type == 'between' and not constraints[1]):
        return True
    elif (check_type == "between"):
        return (int(value) > int(constraints[0]) and int(value) < int(constraints[1]))
    elif (check_type == "lt"):
        return int(value) < int(constraints[0])
    elif (check_type == "gt"):
        return int(value) > int(constraints[0])
    else:
        return str(value) == str(constraints[0])