from django.db import models


class Project(models.Model):
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='projects/')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    def __str__(self):
        return self.title
