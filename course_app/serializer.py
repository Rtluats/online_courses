from rest_framework import serializers

from course_app.models import Course
from lecture_app.serializer import LectureSerializer


class CourseSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True)

    class Meta:
        model = Course
        fields = ('id', 'main_teacher', 'addition_teachers', 'students', 'lectures')
