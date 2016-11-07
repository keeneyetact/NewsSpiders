from django import forms

class SearchForm(forms.Form):
    keys = forms.CharField(100)
