from rest_framework.permissions import BasePermission
from users.models import UserRoles


class IsOwnerOrModerator(BasePermission):
    message = 'Вы не являетесь модератором или владельцем!'

    # def has_permission(self, request, view):
    #     # if view.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy']:
    #     if request.user.is_staff or request.user.is_superuser or request.user == request.get_object().owner\
    #             or request.user.role == UserRoles.MODERATOR and request.method in ['POST', 'DELETE']:
    #         return False
    #     return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        elif request.user.is_superuser:
            return True
        return False
