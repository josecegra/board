from django import forms

from .models import ImageModel

class ButtonForm(forms.Form):
    XAI = forms.CharField()