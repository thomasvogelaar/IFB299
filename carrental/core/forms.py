from django import forms
from bootstrap_datepicker_plus import DatePickerInput

class TransactionsGetForm(forms.Form):
    media_choices = (('table', 'Table'), ('line', 'Line Graph'))
    start_date = forms.DateField(label="Start Date", widget=DatePickerInput(attrs={ 'class': 'form-control' }))
    end_date = forms.DateField(label="End Date", widget=DatePickerInput(attrs={ 'class': 'form-control' }))
    media_type = forms.ChoiceField(choices=media_choices, widget=forms.Select(attrs={ 'class': 'form-control' }))