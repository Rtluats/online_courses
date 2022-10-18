from rest_framework import serializers

from lecture_app.models import Lecture, Homework, HomeworkStudent, Comment


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ('id', 'text')


class LectureSerializer(serializers.ModelSerializer):
    homework = HomeworkSerializer()

    class Meta:
        model = Lecture
        fields = ('id', 'title', 'file', 'homework')


class HomeworkStudentSerializer(serializers.ModelSerializer):
    homework = HomeworkSerializer()

    class Meta:
        model = HomeworkStudent
        fields = ('id', 'homework', 'text', 'student', 'mark')


class CommentSerializer(serializers.ModelSerializer):
    homework_student = HomeworkStudentSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'homework_student', 'message', 'datetime_field')
