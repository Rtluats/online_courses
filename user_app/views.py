from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from permissions import IsOwnerOrReadOnly
from user_app.models import User
from user_app.serializer import UserSerializer

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema


class UserList(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={201: UserSerializer(), 400: "Bad request"}, request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    @swagger_auto_schema(responses={200: UserSerializer(), 404: "No found"})
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: UserSerializer(), 400: "Bad request", 404: "No found"},
                         request_body=UserSerializer)
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "No content", 400: "Bad request", 404: "No found"})
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
