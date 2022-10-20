from rest_framework import serializers

from course_app.models import Course
from user_app.serializer import UserSerializer
from lecture_app.serializer import LectureSerializer


class CourseSerializer(serializers.ModelSerializer):
    main_teacher = UserSerializer()
    addition_teachers = UserSerializer(many=True)
    students = UserSerializer(many=True)

    class Meta:
        model = Course
        fields = ('id', 'main_teacher', 'addition_teachers', 'students')
        depth = 1
