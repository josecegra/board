from django.db import models


# Create your models here.
class TorchModel(models.Model):
    upload = models.FileField()
    name = models.CharField(max_length=255, default = '')

    endpoint = models.CharField(max_length=255, default = '')
    port = models.CharField(max_length=4, default = '')



    path = models.CharField(max_length=255, default = '')
    encoding_dict = models.CharField(max_length=500, default = '')
    is_public = models.BooleanField(default=False)
    username = models.CharField(max_length=255, default = '')

    id = models.AutoField(primary_key=True)


    #api_endpoint = models.CharField(max_length=255, default = '')
    #active = models.BooleanField(default=False)



    CHOICES = [
    ('classification', (
            ('resnet18', 'resnet18'),
            ('resnet34', 'resnet34'),
        )
    ),
    ('segmentation', (
            ('unet', 'unet'),
        )
    ),
    
    ]

    problem_type = models.CharField(
        max_length=8,
        choices=CHOICES,
        default='resnet18',
    )


    def __str__(self):
        return str(self.name)