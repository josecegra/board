from django.db import models

from torch_model_module.models import TorchModel
from datasets.models import DatasetModel

class XAImageModel(models.Model):

    filename = models.CharField(max_length=255, default = '')
    img_file = models.FileField()
    annotation = models.CharField(max_length=255, default = '')
    img_url = models.CharField(max_length=500, default = '')
    #dataset = models.ForeignKey(DatasetModel,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.filename)

# Create your models here.
class ExperimentModel(models.Model):
    name = models.CharField(max_length=255, default = '')
    is_public = models.BooleanField(default=False)
    username = models.CharField(max_length=255, default = '')
    
    # torch_model = models.OneToOneField(TorchModel,on_delete=models.CASCADE,null=True,blank=True)
    # dataset = models.OneToOneField(DatasetModel,on_delete=models.CASCADE,null=True,blank=True)



    torch_model = models.ManyToManyField(TorchModel,related_name='experiments')
    dataset = models.ManyToManyField(DatasetModel,related_name='experiments')   


    def __str__(self):
        return str(self.name)