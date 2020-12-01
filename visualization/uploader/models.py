from django.db import models

# Create your models here.
class Doc(models.Model):
    upload = models.ImageField()
    image_url = models.CharField(max_length=255, default = '')
    user = models.CharField(max_length=255, default = '')

    def __str__(self):
        return str(self.pk)