from django.db import models


# Create your models here.
class TorchModel(models.Model):
    upload = models.FileField()
    #weights_url = models.CharField(max_length=255, default = '')
    #user = models.CharField(max_length=255, default = '')
    name = models.CharField(max_length=255, default = '')
    is_public = models.BooleanField(default=False)
    username = models.CharField(max_length=255, default = '')

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
        return str(self.pk)