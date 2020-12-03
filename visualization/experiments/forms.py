from django import forms

from .models import ExperimentModel
class ExperimentForm(forms.ModelForm):
    class Meta:
        model = ExperimentModel
        fields = [ 'name','is_public']
  

