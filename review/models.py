from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.conf import settings
from taggit.managers import TaggableManager
# Create your models here.

class Review(models.Model):
    title = models.CharField(verbose_name='TITLE', max_length=50)
    movie_title = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    spo = models.CharField(max_length=50,null=True)
    content = RichTextUploadingField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    tag = TaggableManager(blank=True)
    read_cnt = models.IntegerField('READ_CNT', default=0)
    SNImg = models.ImageField(null=True)

    class Mete:
        ordering = ('-create_date',) #orderby 절, -이면 내림차순순 컴마한거봐서 튜플임을 알수있음
        #ordering을 함으로써 결국 최신순으로 정렬되는덧
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('review:redetail')

    def get_previous(self):
        return self.get_previous_by_create_date()
    def get_next(self):
        return self.get_next_by_create_date()

    @property
    def update_counter(self):
         self.read_cnt = self.read_cnt + 1
         self.save()

class Detgle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class ReviewAttachFile(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                             related_name="files", verbose_name='Review', blank=True, null=True)

    upload_file = models.FileField(upload_to="%Y/%m/%d",
                                   null=True, blank=True, verbose_name='파일')

    filename = models.CharField(max_length=64, null=True,
                                verbose_name='첨부파일명')

    content_type = models.CharField(max_length=128, null=True,
                                    verbose_name='MIME TYPE')

    size = models.IntegerField('파일 크기')

    def __str__(self):
        return self.filename