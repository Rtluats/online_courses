from rest_framework import permissions


class IsOwnerOrReadOnlyForStudents(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST' and 'TEACHER' in request.user.roles:
            return True

        if request.method == permissions.SAFE_METHODS and request.user in obj.students_of_course:
            return True

        return request.user == obj.owner or request.user in obj.teachers


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == permissions.SAFE_METHODS:
            return True
        return request.user == obj.owner


class IsOwnerOfHomeworkStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user in obj.teachers or request.user in obj.students_of_course
