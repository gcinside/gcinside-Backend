from django.db import models

# Create your models here.
from api.accounts.models import User


class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField

    def __str__(self) -> str:
        return self.gallery_name + " 갤러리"
