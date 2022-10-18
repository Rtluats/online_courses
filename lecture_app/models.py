from django.db import models
from django.contrib.auth.models import User

from course_app.models import Course


# Create your models here.


class Homework(models.Model):
    text = models.TextField(blank=False)


class Lecture(models.Model):
    title = models.CharField(max_length=256, blank=False)
    file = models.FileField()
    homework = models.OneToOneField(Homework, on_delete=models.CASCADE, null=True)

    def __search_course(self):
        return Course.objects.filter(lectures__pk=self.pk).first()

    @property
    def owner(self):
        return self.__search_course().owner

    @property
    def teachers(self):
        return self.__search_course().teachers

    @property
    def students_of_course(self):
        return self.__search_course().students_of_course


class HomeworkStudent(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    text = models.TextField(blank=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.IntegerField()


class Comment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    homework_student = models.ForeignKey(HomeworkStudent, on_delete=models.CASCADE)
    message = models.TextField()
    datetime_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('datetime_field',)
