from django import forms


class SearchForm(forms.Form):
    text = forms.CharField(max_length=40, required=True, label='поиск')