from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response

from teaching.models import *
from teaching.serializers import UserProfileSerializer

from teaching.response_content import ResponseContent
from teaching.unit.permission import RootPermission

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from teaching.unit.ValidView import ValidApiView


class UserBindProfile(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, RootPermission]


    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12017)
        state = status.HTTP_200_OK
        detail = self.readiness(request)

        result = {}
        count = 0
        formerly = 0
        refreshName = 0
        add = 0
        surplus = 0
        try:
            users = User.objects.all()
            count = len(users)
            for user in users:
                if not hasattr(user, 'userteachingprofile'):
                    role = 0
                    if user.is_superuser > 0:
                        role = 100
                    serializer = UserProfileSerializer(data={
                        'name': user.first_name + user.last_name,
                        'role': role,
                        'user': user.id
                    }, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        add += 1
                    else:
                        result[user.username] = serializer.errors
                        surplus += 1
                else:
                    formerly += 1
                    if user.first_name + user.last_name:
                        serializer = UserProfileSerializer(user.userteachingprofile, data={
                            'name': user.first_name + user.last_name,
                        }, partial=True)
                        if serializer.is_valid():
                            serializer.save()
            response.data = {
                'count': count,
                'formerly': formerly,
                'add': add,
                'surplus': surplus,
                'reason': result
            }
        except Exception as e:
            response.refresh(code=604, description=10551, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)
