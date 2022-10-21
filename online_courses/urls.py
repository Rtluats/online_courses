"""online_courses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from course_app.views import CourseList, CourseDetail
from lecture_app.views import LectureList, HomeworkStudentList, LectureDetail, HomeworkStudentDetail
from user_app.views import UserList, UserDetail

schema_view = get_schema_view(
    openapi.Info(
        title="Online Courses API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="rtluats@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('users/', UserList.as_view()),
    path('user/<int:pk>', UserDetail.as_view()),
    path('courses/', CourseList.as_view()),
    path('courses/<int:pk>', CourseDetail.as_view()),
    path('lectures/', LectureList.as_view()),
    path('lectures/<int:pk>', LectureDetail.as_view()),
    path('homework_students/', HomeworkStudentList.as_view()),
    path('homework_students/<int:pk>', HomeworkStudentDetail.as_view())
]
