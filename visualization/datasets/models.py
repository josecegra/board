from django.db import models

class ImageModel(models.Model):

    filename = models.CharField(max_length=255, default = '')
    img_file = models.FileField()
    annotation = models.CharField(max_length=255, default = '')
    img_url = models.CharField(max_length=500, default = '')
    #dataset = models.ForeignKey(DatasetModel,on_delete=models.CASCADE,null=True,blank=True)

    

    def __str__(self):
        return str(self.filename)

# Create your models here.
class DatasetModel(models.Model):

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

    img_list = models.ManyToManyField(ImageModel)

    def __str__(self):
        return str(self.name)


