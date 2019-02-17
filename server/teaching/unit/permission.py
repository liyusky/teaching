from rest_framework.permissions import BasePermission

class TeacherPermission(BasePermission):
    message = '您不具有教师权限！'
    def has_permission(self, request, view):
        response = False
        user = request.user
        if hasattr(user, 'userteachingprofile'):
            profile = user.userteachingprofile
            if int(profile.role) > 0 and int(profile.role) < 99:
                response = True
        return response


class ManagerPermission(BasePermission):
    message = '您不具有管理员权限！'

    def has_permission(self, request, view):
        response = False
        user = request.user
        if hasattr(user, 'userteachingprofile'):
            profile = user.userteachingprofile
            if int(profile.role) in [99, 100]:
                response = True
        return response


class StudentPermission(BasePermission):
    message = '您不具有学生权限！'

    def has_permission(self, request, view):
        response = False
        user = request.user
        if hasattr(user, 'userteachingprofile'):
            profile = user.userteachingprofile
            if int(profile.role) == 0:
                response = True
        return response


class RootPermission(BasePermission):
    message = '您不具有root权限！'

    def has_permission(self, request, view):
        response = False
        user = request.user
        if hasattr(user, 'userteachingprofile'):
            profile = user.userteachingprofile
            if int(profile.role) == 100:
                response = True
        return response
