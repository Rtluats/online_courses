from rest_framework import permissions


class IsOwnerOrReadOnlyForStudents(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == permissions.SAFE_METHODS and request.user in obj.students_of_course:
            return True

        return request.user == obj.owner or request.user in obj.teachers
