from django import forms

from .models import TorchModel
class TorchModelForm(forms.ModelForm):
    class Meta:
        model = TorchModel
        fields = [ 'upload','name','problem_type','is_public']
  

