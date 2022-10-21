from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from permissions import IsOwnerOrReadOnlyForStudents
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from course_app.models import Course
from course_app.serializer import CourseSerializer


class CourseList(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyForStudents)

    @swagger_auto_schema(responses={200: CourseSerializer(many=True)})
    def get(self, request):
        courses = Course.course_by_user.get_queryset(request.user.id).all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={201: CourseSerializer(), 400: "Bad request"}, request_body=CourseSerializer)
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

    @swagger_auto_schema(responses={200: CourseSerializer(), 404: "Not found"})
    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: CourseSerializer(),  404: "Not found",  400: "Bad request"},
                         request_body=CourseSerializer)
    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "No content", 404: "Not found"},
                         request_body=CourseSerializer)
    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
