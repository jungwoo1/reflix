from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.conf import settings
# Create your models here.

class Review(models.Model):
    title = models.CharField(verbose_name='TITLE', max_length=50)
    content = RichTextUploadingField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title