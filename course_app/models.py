from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Course(models.Model):
    main_teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    addition_teachers = models.ManyToManyField(User)
    students = models.ManyToManyField(User)

    @property
    def owner(self):
        return self.main_teacher

    @property
    def teachers(self):
        return self.addition_teachers

    @property
    def students_of_course(self):
        return self.students
