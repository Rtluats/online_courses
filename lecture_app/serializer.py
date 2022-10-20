from rest_framework import serializers

from lecture_app.models import Lecture, Homework, HomeworkStudent, Comment
from user_app.serializer import UserSerializer
from course_app.serializer import CourseSerializer


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ('id', 'text')


class LectureSerializer(serializers.ModelSerializer):
    homework = HomeworkSerializer()
    course = CourseSerializer()

    class Meta:
        model = Lecture
        fields = ('id', 'title', 'file', 'homework', 'course')
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    homework_student = serializers.PrimaryKeyRelatedField()
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'homework_student', 'message', 'datetime_field')
        read_only_fields = ('datetime_field',)
        depth = 1


class HomeworkStudentSerializer(serializers.ModelSerializer):
    homework = HomeworkSerializer()
    student = UserSerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model = HomeworkStudent
        fields = ('id', 'homework', 'text', 'student', 'mark', 'comments')
        depth = 1
