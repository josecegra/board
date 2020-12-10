from django.db import models

from torch_model_module.models import TorchModel
from datasets.models import DatasetModel

# Create your models here.
class ExperimentModel(models.Model):
    name = models.CharField(max_length=255, default = '')
    is_public = models.BooleanField(default=False)
    username = models.CharField(max_length=255, default = '')
    
    torch_model = models.OneToOneField(TorchModel,on_delete=models.CASCADE,null=True,blank=True)
    dataset = models.OneToOneField(DatasetModel,on_delete=models.CASCADE,null=True,blank=True)

    # torch_model = models.ManyToManyField(TorchModel)
    # dataset = models.ManyToManyField(DatasetModel)   


    def __str__(self):
        return str(self.name)