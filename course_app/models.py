from django.db import models
from django.db.models import Q

from user_app.models import User


class Manager(models.Manager):
    def get_queryset(self, user_id):
        return super().get_queryset().filter(Q(main_teacher__pk=user_id) |
                                             Q(addition_teachers__pk=user_id) |
                                             Q(students__pk=user_id)).distinct()


class Course(models.Model):
    main_teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_main_teacher")
    addition_teachers = models.ManyToManyField(User, related_name="course_addition_teachers")
    students = models.ManyToManyField(User, related_name="course_students")
    course_by_user = Manager()

    @property
    def owner(self):
        return self.main_teacher

    @property
    def teachers(self):
        return self.addition_teachers

    @property
    def students_of_course(self):
        return self.students
