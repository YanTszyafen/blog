from django.db import models
from django.utils import timezone
# Create your models here.

class ArticleCategory(models.Model):

    title = models.CharField(max_length=100, blank=True)

    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    #admin site display, easy to debug and view objects
    class Meta:
        db_table = 'tb_category' #modify table name
        verbose_name = 'Category management' #admin site display
        verbose_name_plural = verbose_name