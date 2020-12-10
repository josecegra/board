from django import forms
from torch_model_module.models import TorchModel
from .models import ExperimentModel
class ExperimentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ExperimentForm, self).__init__(*args, **kwargs)

        self.fields['is_public'].required = False
        self.fields['name'].widget.attrs.update({'class' : 'short-width'})

    #torch_model = forms.ModelChoiceField(queryset=TorchModel.objects.all())

    class Meta:
        model = ExperimentModel
        fields = [ 'name','torch_model','dataset','is_public',]

    # torch_model = forms.ModelMultipleChoiceField(
    #     queryset=TorchModel.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )

  

