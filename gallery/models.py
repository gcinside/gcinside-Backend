from django.db import models

# Create your models here.
class Gallery(models.Model):
    gallery_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.gallery_name + ' 갤러리'