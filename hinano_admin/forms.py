from django import forms

class Topics_form(forms.Form):
    id = forms.CharField(label='ID',max_length=4)
    title = forms.CharField(label='Nama',max_length=100)
    description = forms.CharField(label='Nama',max_length=100)
