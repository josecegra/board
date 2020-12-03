from django.db import models


# Create your models here.
class DatasetModel(models.Model):
    #upload = models.FileField()
    #weights_url = models.CharField(max_length=255, default = '')
    #user = models.CharField(max_length=255, default = '')
    name = models.CharField(max_length=255, default = '')
    
    username = models.CharField(max_length=255, default = '')

    CHOICES = [
    ('none','none'),
    ('classification','classification'),
    ('segmentation','segmentation'),
    ]

    problem_type = models.CharField(
        max_length=20,
        choices=CHOICES,
        default='none',
    )

    images_path = models.CharField(max_length=255, default = '')
    annotations_path = models.CharField(max_length=255, default = '')
    annotations_upload = models.FileField()


    is_public = models.BooleanField(default=False)


    def __str__(self):
        return str(self.name)