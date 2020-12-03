from django.db import models

from torch_model_module.models import TorchModel
from datasets.models import DatasetModel


# def get_models(username):
#     obj_list = TorchModel.objects.filter(username=username)
#     print(type(obj_list))


# Create your models here.
class ExperimentModel(models.Model):
    #upload = models.FileField()
    #weights_url = models.CharField(max_length=255, default = '')
    #user = models.CharField(max_length=255, default = '')
    name = models.CharField(max_length=255, default = '')
    is_public = models.BooleanField(default=False)
    username = models.CharField(max_length=255, default = '')

    # CHOICES = [
    # ('classification','classification'),
    # ('segmentation','segmentation'),
    
    # ]

    # problem_type = models.CharField(
    #     max_length=20,
    #     choices=CHOICES,
    #     default='classification',
    # )

    MODEL_CHOICES = [
    ('classification','classification'),
    ('segmentation','segmentation'),]

    #get_models(username)
    
    torch_model = models.ForeignKey(TorchModel,on_delete=models.CASCADE,null=True,blank=True)
    dataset = models.ForeignKey(DatasetModel,on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return str(self.name)