from django import forms


class LocalizationForm(forms.Form):
    latitude = forms.CharField(label='Latitude', max_length=12,)
    longitude = forms.CharField(label='Longitude', max_length=12)
