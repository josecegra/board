from django import forms

from .models import TorchModel
class TorchModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(TorchModelForm, self).__init__(*args, **kwargs)
        self.fields['is_public'].required = False
        
        self.fields['path'].widget.attrs.update({'class' : 'long-width'})
        self.fields['encoding_dict'].widget.attrs.update({'class' : 'long-width'})
        self.fields['name'].widget.attrs.update({'class' : 'short-width'})
        self.fields['problem_type'].widget.attrs.update({'class' : 'short-width'})

    class Meta:
        model = TorchModel
        fields = [ 'name','path','encoding_dict','problem_type','is_public']
  

