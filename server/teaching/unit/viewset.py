from teaching.unit.permission import TeacherPermission
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from teaching.response_content import ResponseContent
from rest_framework import status
from rest_framework.response import Response


class GetList(ModelViewSet):
    api_name = ''
    auth_dict = {}
    success_code = {}
    fail_code = {}
    @detail_route(methods=['get'], url_name=api_name + '-list', authentication_classes=auth_dict['get'])
    def get_list(self, request, pk=None):
        response = ResponseContent(code=200, token=request.auth, description=self.success_code['get'])
        state = status.HTTP_200_OK

        instance = self.get_object()
        serializer = self.get_serializer(instance, many=True)
        response.data = serializer.data

        return Response(response.content(), status=state)


class AddInstance(ModelViewSet):
    api_name = ''
    auth_dict = {}
    success_code = {}
    fail_code = {}
    @detail_route(methods=['post'], url_name='add-' + api_name, authentication_classes=auth_dict['post'])
    def add_instance(self, request, pk=None):
        response = ResponseContent(code=200, token=request.auth, description=self.success_code['post'])
        state = status.HTTP_200_OK

        serializer = self.get_serializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=604, description=self.fail_code['post'], error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class UpdateInstance(ModelViewSet):
    api_name = ''
    auth_dict = {}
    success_code = {}
    fail_code = {}
    @detail_route(methods=['patch'], url_name='update-course', authentication_classes=auth_dict['patch'])
    def update_instance(self, request, pk=None):
        response = ResponseContent(code=200, token=request.auth, description=self.success_code['patch'])
        state = status.HTTP_200_OK

        instance = request.user[self.api_name]
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=604, description=self.fail_code['post'], error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class ManagerModelViewSet(GetList, AddInstance, UpdateInstance):
    permission_classes = [TeacherPermission]
