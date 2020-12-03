from django import forms

from .models import ExperimentModel
class ExperimentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ExperimentForm, self).__init__(*args, **kwargs)

        self.fields['is_public'].required = False
        self.fields['name'].widget.attrs.update({'class' : 'short-width'})

    class Meta:
        model = ExperimentModel
        fields = [ 'name','is_public']
  

