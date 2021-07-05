from rest_framework import permissions


class IsUserOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_active:
            return True
        else:
            return False

        # Write permissions are only allowed to the owner of the snippet.
        # return obj.owner == request.user