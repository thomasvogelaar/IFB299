from django import forms
from bootstrap_datepicker_plus import DatePickerInput

class TransactionsGetForm(forms.Form):
    """ This form is found at the top of the transctions list """
    media_choices = (('table', 'Table'), ('line', 'Line Graph'), ('pie', 'Pie Graph'), ('bar', 'Bar Graph'))
    start_date = forms.DateField(label="Start Date", widget=DatePickerInput(attrs={ 'class': 'form-control' }))
    end_date = forms.DateField(label="End Date", widget=DatePickerInput(attrs={ 'class': 'form-control' }))
    media_type = forms.ChoiceField(choices=media_choices, widget=forms.Select(attrs={ 'class': 'form-control' }))

class CarRecommendForm(forms.Form):
    """ This is the car recommendation form """
    make = forms.CharField(required=False)
    model = forms.CharField(required=False)
    car_age = forms.ChoiceField(required=False)
    engine_size = forms.CharField(required=False)
    fuel_system = forms.CharField(required=False)
    power = forms.CharField(required=False)
    seats = forms.CharField(required=False)
    body_type = forms.CharField(required=False)
    drive = forms.CharField(required=False)
    car_size = forms.ChoiceField(required=False)

    car_size.choices = (
        ("< 2553", "Small"),
        ("BETWEEN 2553 AND 2877", "Medium"),
        ("> 2877", "Large"))
    car_age.choices = (
        ("> 5", "> 5 years"),
        ("BETWEEN 5 AND 10", "5 - 10 years"),
        ("BETWEEN 10 AND 15", "10 - 15 years"),
        ("BETWEEN 15 AND 20", "15 - 20 years"),
        ("BETWEEN 20 AND 25", "20 - 25 years"),
        ("BETWEEN 25 AND 30", "25 - 30 years"),
        ("< 30", "< 30 years"))
