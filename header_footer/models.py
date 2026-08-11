from django.db import models


class Header(models.Model):
    title = models.CharField(max_length=100)
    followers = models.IntegerField()
    users = models.IntegerField()
    link = models.URLField()
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class FooterText(models.Model):
    title1 = models.CharField(max_length=100)
    title2 = models.CharField(max_length=100)
    title3 = models.CharField(max_length=100)
    title4 = models.CharField(max_length=100)

    def __str__(self):
        return self.title1


class Footer(models.Model):
    logo = models.ImageField(upload_to='footer_image/')
    title = models.CharField(max_length=100)
    description = models.TextField()
    footer_text = models.ForeignKey(
        FooterText,
        on_delete=models.CASCADE,
        related_name='footer',
    )

    def __str__(self):
        return self.title
