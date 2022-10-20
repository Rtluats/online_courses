from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from permissions import IsOwnerOrReadOnlyForStudents
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from course_app.models import Course
from course_app.serializer import CourseSerializer


class CourseList(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyForStudents)

    def get(self, request):
        courses = Course.course_by_user.get_queryset(request.user.id).all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetail(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyForStudents)

    def get_object(self, pk):
        return get_object_or_404(Course, pk=pk)

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
