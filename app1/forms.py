from django import forms

class loginForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    pass1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput)