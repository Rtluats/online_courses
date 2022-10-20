from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

from permissions import IsOwnerOrReadOnlyForStudents, IsOwnerOfHomeworkStudent

from lecture_app.models import Lecture, HomeworkStudent
from lecture_app.serializer import LectureSerializer, HomeworkStudentSerializer
from user_app.models import User
from user_app.serializer import UserSerializer


class LectureList(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyForStudents)
    parser_classes = (FileUploadParser,)

    def get(self, request):
        lectures = Lecture.lecture_by_user.get_queryset(request.user.id).all()
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LectureSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            if obj.homework:
                for student in obj.students_of_course:
                    HomeworkStudent.objects.create(homework=obj.homework, student=student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LectureDetail(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyForStudents)
    parser_classes = (FileUploadParser,)

    def get_object(self, pk):
        return get_object_or_404(Lecture, pk=pk)

    def get(self, request, pk):
        lecture = self.get_object(pk)
        serializer = LectureSerializer(lecture)
        return Response(serializer.data)

    def put(self, request, pk):
        lecture = self.get_object(pk)
        serializer = LectureSerializer(lecture, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            if not lecture.homework and obj.homework:
                for student in obj.students_of_course:
                    HomeworkStudent.objects.create(homework=obj.homework, student=student)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        lecture = self.get_object(pk)
        lecture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HomeworkStudentList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, is_done=None):
        if is_done is None:
            homeworks = HomeworkStudent.objects.all()
        else:
            homeworks = HomeworkStudent.objects.filter(is_done=is_done).all()
        serializer = HomeworkStudentSerializer(homeworks, many=True)
        return Response(serializer.data)


class HomeworkStudentDetail(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOfHomeworkStudent)

    def get_object(self, pk):
        return get_object_or_404(HomeworkStudent, pk=pk)

    def get(self, request, pk):
        homework_student = self.get_object(pk)
        serializer = HomeworkStudentSerializer(homework_student)
        return Response(serializer.data)

    def put(self, request, pk):
        user: User = request.user
        data = request.data
        if 'comments' in data:
            for comment in data['comments']:
                if 'id' not in comment or 'user' not in comment:
                    comment['user'] = UserSerializer(user).data
        homework_student: HomeworkStudent = self.get_object(pk)
        serializer_new = HomeworkStudentSerializer(homework_student, data=data)
        serializer_old = HomeworkStudentSerializer(homework_student)
        if ['STUDENT'] in user.roles and homework_student.student.id == user.id:
            serializer_old.data['text'] = serializer_new.data['text']
            serializer_new = serializer_old
        if ['TEACHER'] in user.roles and homework_student.student.id != user.id:
            serializer_new.data['text'] = serializer_old.data['text']
        if serializer_new.is_valid():
            serializer_new.save()
            return Response(serializer_new.data)
        return Response(serializer_new.errors, status=status.HTTP_400_BAD_REQUEST)

