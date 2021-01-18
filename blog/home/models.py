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


from users.models import User
from django.utils import timezone
class Article(models.Model):
    #on_delete: When the data in the user table is deleted, the article information is also deleted synchronously
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    #author = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='article/%Y%m%d/',blank=True)
    title = models.CharField(max_length=120,blank=True)
    category = models.ForeignKey(ArticleCategory,null=True,blank=True,on_delete=models.CASCADE,related_name='article')
    #tags = models.CharField(max_length=50,blank=True)
    #summary = models.CharField(max_length=600,null=False,blank=False)
    content = models.TextField()
    total_views = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    #Modify the table name and configuration information.
    class Meta:
        db_table = 'tb_article'
        ordering = ('-created',)
        verbose_name = 'Article management'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
