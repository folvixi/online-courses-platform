from django import forms

class EnrollForm(forms.Form):
    name = forms.CharField(max_length=100, label='Ваше имя')
    email = forms.EmailField(label='Email')
    course = forms.CharField(widget=forms.HiddenInput())  # передаём slug курса
