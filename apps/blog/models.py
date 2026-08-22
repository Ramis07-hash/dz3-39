from django.db import models

# Create your models here.

class BlogCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)


class Blog(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    category = models.ForeignKey(BlogCategory,
                                 on_delete=models.CASCADE,
                                 related_name='category',)
    