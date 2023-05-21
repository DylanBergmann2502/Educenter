from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Any user can list or retrieve the object(s),
    but only staff users (authenticated first, of course) can create, update, and delete them
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff


class IsTeacherOwnerOrReadOnly(permissions.BasePermission):
    """
    Any user can list or retrieve the object(s),
    but only teacher users (authenticated first, of course) can create,
    and only if that teacher user is owner of the object, can he/she update or delete it
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated \
            and request.user.is_teacher

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated \
            and request.user.is_teacher \
            and request.user == obj.teacher.user


# I kept this just for me to understand these permissions later on in retrospect,
# it works exactly the same as the current one in use
class OldIsStaffOrReadOnly(permissions.BasePermission):
    """
    Any user can list or retrieve the object(s),
    but only staff users (authenticated first, of course) can create, update, and delete them
    """

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated and request.user.is_staff
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated and request.user.is_staff
        return False


class OldIsTeacherOwnerOrReadOnly(permissions.BasePermission):
    """
    Any user can list or retrieve the object(s),
    but only teacher users (authenticated first, of course) can create,
    and only if that teacher user is owner of the object, can he/she update or delete it
    """

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated \
                and request.user.is_teacher
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action == 'create':
            return request.user.is_authenticated \
                and request.user.is_teacher
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_authenticated \
                and request.user.is_teacher \
                and request.user == obj.teacher.user
        return False