from django import forms
from bootstrap_datepicker_plus import DatePickerInput

class TransactionsGetForm(forms.Form):
    start_date = forms.DateField(label="Start Date", widget=DatePickerInput(attrs={'class': 'form-control' }))
    end_date = forms.DateField(label="End Date", widget=DatePickerInput(attrs={'class': 'form-control' }))