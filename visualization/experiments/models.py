from django.db import models

from torch_model_module.models import TorchModel
from datasets.models import DatasetModel

# Create your models here.
class ExperimentModel(models.Model):
    name = models.CharField(max_length=255, default = '')
    is_public = models.BooleanField(default=False)
    username = models.CharField(max_length=255, default = '')
    
    torch_model = models.ForeignKey(TorchModel,on_delete=models.CASCADE,null=True,blank=True)
    dataset = models.ForeignKey(DatasetModel,on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return str(self.name)