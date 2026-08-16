from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    students_count = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    duration_min = models.PositiveIntegerField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return f'{self.course.title}: {self.title}'

#Урок 4. Class-Based Views в DRF, Mixins, кастомизация CRUD и вложенные URL.