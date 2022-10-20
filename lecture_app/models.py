from django.db import models

from user_app.models import User
from course_app.models import Course, Manager


class Homework(models.Model):
    text = models.TextField(blank=False)


class Lecture(models.Model):
    title = models.CharField(max_length=256, blank=False)
    file = models.FileField()
    homework = models.OneToOneField(Homework, on_delete=models.CASCADE, null=True, related_name="lecture")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecture_by_user = Manager()

    @property
    def owner(self):
        return self.course.owner

    @property
    def teachers(self):
        return self.course.teachers

    @property
    def students_of_course(self):
        return self.course.students_of_course


class HomeworkStudent(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    text = models.TextField(blank=True, default='')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.IntegerField(default=0)

    @property
    def get_lecture(self):
        return self.homework.lecture

    @property
    def owner(self):
        return self.get_lecture.owner

    @property
    def teachers(self):
        return self.get_lecture.teachers

    @property
    def students(self):
        return [self.student]


class Comment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    homework_student = models.ForeignKey(HomeworkStudent, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()
    datetime_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-datetime_field',)
