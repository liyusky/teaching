import uuid

from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from teaching.models import User
from teaching.serializers import UserSerializer, UserProfileSerializer

from teaching.unit.permission import ManagerPermission
from teaching.response_content import ResponseContent

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from teaching.unit.ValidView import ValidApiView
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, login, logout
from kudingmao.stage_controller import login_init

class LoginByPassword(ValidApiView):
    authentication_classes = []
    permission_classes = []
    process_list = ['no-jwt', 'exist-account', 'current-account', 'image-code', 'refresh-login']
    format_keys = ['phone', 'password', 'imageCode']
    check_list = {
        'phone': 'shortAccount',
        'password': 'password',
        'imageCode': 'imageCode',
    }

    # 登录
    def post(self, request, *args, **kwargs):
        params = request.data
        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        token = self.get_jwt_token(detail['user'])

        response = self.auth(request, detail['user'], params['password'])
        if isinstance(response, ResponseContent):
            return Response(response.content(), status=status.HTTP_401_UNAUTHORIZED)


        serializer = UserProfileSerializer(detail['profile'])
        response = ResponseContent(
            code=200,
            description=12000,
            token=token,
            data=serializer.data
        )
        return Response(response.content(), status=status.HTTP_200_OK)

    def get_jwt_token(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def auth(self, request, user, password):
        response = True

        user = authenticate(username=user.username, password=password)
        if user is None:
            response = ResponseContent(code=401, description=10103, error=10103)
        elif user is not None:
            login_init(user)
            if user.is_active:
                login(request, user)
            else:
                response = ResponseContent(code=601, description=10150, error=10150)


        return response


class LoginBySMSCaptcha(ValidApiView):
    scene = 0
    authentication_classes = []
    permission_classes = []
    process_list = ['no-jwt', 'sms-code', 'exist-account', 'current-account']
    format_keys = ['phone', 'smsCode']
    check_list = {
        'phone': 'phone',
        'smsCode': 'smsCode',
    }

    # 登录
    def post(self, request, *args, **kwargs):
        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        token = self.get_jwt_token(detail['user'])
        response = self.auth(request, detail['user'])
        if isinstance(response, ResponseContent):
            return Response(response.content(), status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserProfileSerializer(detail['profile'])
        response = ResponseContent(
            code=200,
            description=12000,
            token=token,
            data=serializer.data
        )
        return Response(response.content(), status=status.HTTP_200_OK)

    def get_jwt_token(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def auth(self, request, user):
        response = True
        login_init(user)
        if user.is_active:
            login(request, user)
        else:
            response = ResponseContent(code=601, description=10150, error=10150)


        return response


class Register(ValidApiView):
    scene = 1
    authentication_classes = []
    permission_classes = []
    process_list = ['no-jwt', 'sms-code', 'no-exist-account']
    format_keys = ['account', 'password', 'smsCode']
    check_list = {
        'account': 'phone',
        'password': 'password',
        'smsCode': 'smsCode'
    }
    # 注册
    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=601, description=10500)
        state = status.HTTP_500_INTERNAL_SERVER_ERROR

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        params = request.data

        serializer = UserSerializer(data={
            'username': params['account'],
            'password': params['password']
        }, partial=True)

        if serializer.is_valid():
            user = serializer.save()
            serializer = UserProfileSerializer(data={
                'user': user.id,
                'phone': params['account']
            }, partial=True)
            if serializer.is_valid():
                profile = serializer.save()
                token = self.get_jwt_token(user)

                result = self.auth(request, user)
                if isinstance(result, ResponseContent):
                    return Response(result.content(), status=status.HTTP_401_UNAUTHORIZED)

                response.refresh(code=200, token=token, description=12001, data=serializer.data)
                state = status.HTTP_200_OK
            else:
                response.error = serializer.errors
        else:
            response.error = serializer.errors

        return Response(response.content(), status=state)

    def get_jwt_token(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


    def auth(self, request, user):
        response = True

        login_init(user)
        if user.is_active:
            login(request, user)
        else:
            response = ResponseContent(code=601, description=10150, error=10150)

        return response


class ForgetPassword(ValidApiView):
    scene = 2
    authentication_classes = []
    permission_classes = []
    process_list = ['no-jwt', 'sms-code', 'exist-account', 'current-account']
    format_keys = ['phone', 'password', 'smsCode']
    check_list = {
        'phone': 'phone',
        'password': 'password',
        'smsCode': 'smsCode',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(mark=False, code=200, token=request.auth, description=12002)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)


        serializer = UserSerializer(
            detail['user'],
            data={'password': request.data['password']},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=601, description=12002, error=serializer.errors)
            state = status.HTTP_501_NOT_IMPLEMENTED

        return Response(response.content(), status=state)


class Logout(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, description=12054)
        state = status.HTTP_200_OK

        logout(request)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(request.user)
        token = jwt_encode_handler(payload)

        return Response(response.content(), status=state)
