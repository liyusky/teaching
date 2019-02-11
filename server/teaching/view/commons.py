from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from teaching.models import User
# from teaching.serializers import GetHomeworkDetailSerializer

from teaching.captcha import Captcha
from teaching.sms_captcha import SMSCaptcha
from teaching.throttle import SMSSendThrottle
from teaching.response_content import ResponseContent
from kudingmao.models import GameStage as MaoStage, UserStagesStatistic as MaoScore, JudgeRecord as MaoRecord
from kudingmao.stage_controller import accessChapter as mao_access_chapter, isChapterFinished as mao_chapter_finish, \
    isChapterUnlocked as mao_chapter_unlock
from teaching.serializers import CommentSerializer, UserSerializer, MaoStageSerializer, MaoScoreSerializer, \
    MaoRecordSerializer, UserProfileSerializer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from teaching.unit.ValidView import ValidApiView

class CaptchaView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, *args, **kwargs):
        captcha = Captcha(request)
        return HttpResponse(captcha.display(), content_type="images/jpg")


class SMSCaptchaView(ValidApiView):
    throttle_classes = [SMSSendThrottle, ]
    process_list = ['no-jwt', 'exist-account', 'no-exist-account', 'image-code']
    format_keys = ['phone', 'scene', 'imageCode']
    check_list = {
        'phone': 'phone',
        'imageCode': 'imageCode',
        'scene': 'range3',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, description=12003)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        sms_captcha = SMSCaptcha()
        result = sms_captcha.send(request.data['phone'], int(request.data['scene']))
        if isinstance(result, ResponseContent):
            response = result
        if response.code > 300 or response.status == 'sms':
            state = status.HTTP_200_OK
        return Response(response.content(), status=state)


class SourceCode(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    process_list = []
    format_keys = ['mrcid']
    check_list = {
        'mrcid': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12004)
        state = status.HTTP_200_OK
        params = request.data
        try:
            record = MaoRecord.objects.filter(id=request.data['mrcid'])
            if record.exists():
                record = record.last()
                response.data = {
                    'code': record.origin_code,
                    'result': record.result,
                    'output': record.output
                }
        except Exception as e:
            response.refresh(code=602, description=10557, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


# 评语
class CommentSingle(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    process_list = ['exist-student']
    format_keys = ['sid', 'hid']
    check_list = {
        'sid': 'id',
        'hid': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12005)
        state = status.HTTP_200_OK
        params = request.data

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            comment = Comment.objects.filter(homework=params['hid'], student=params['sid'])
            response.data = CommentSerializer(comment, many=True).data
        except Exception as e:
            response.refresh(code=602, description=10503, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


# class SchoolList(ValidApiView):
#     authentication_classes = [JSONWebTokenAuthentication, ]
#     permission_classes = [IsAuthenticated, ]
#     format_keys = ['enable', 'level']
#     check_list = {
#         'level': 'range5',
#         'enable': 'range3'
#     }

#     def post(self, request, *args, **kwargs):
#         response = ResponseContent(code=200, token=request.auth, description=12006)
#         state = status.HTTP_200_OK
#         params = request.data
#         try:
#             if int(params['enable']) == 2:
#                 school = School.objects.all()
#             else:
#                 if 'level' in params:
#                     school = School.objects.filter(enable=params['enable'], level=params['level'])
#                 else:
#                     school = School.objects.filter(enable=params['enable'])
#             serializer = SchoolSerializer(school, many=True)
#             response.data = serializer.data
#         except Exception as e:
#             response.refresh(mark=True, code=602, description=10504, error=e.__str__())
#             state = status.HTTP_500_INTERNAL_SERVER_ERROR

#         return Response(response.content(), status=state)


class UpdateAccount(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    # process_list = ['exist-school']
    check_list = {
        'name': 'name',
        'age': 'id',
        'sex': 'range2',
        # 'school': 'id',
        # 'password': 'password',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12007)
        state = status.HTTP_200_OK
        params = request.data

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        user = detail['user']
        profile = detail['profile']

        if 'name' in params:
            serializer = UserSerializer(user, data={
                'first_name': params['name'][0:1],
                'last_name': params['name'][1:]
            }, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                response.refresh(code=601, description=10505, error=serializer.errors)
                state = status.HTTP_500_INTERNAL_SERVER_ERROR

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response.data = serializer.data
        else:
            response.refresh(code=601, description=10505, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)



class GameUrl(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    process_list = ['exist-student', ]
    format_keys = ['student', 'gcid']
    check_list = {
        'gcid': 'id',
        'student': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12050)
        state = status.HTTP_200_OK
        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        student = detail['student']
        url = mao_access_chapter(student.user, request.data['gcid'])
        if url:
            response.data = url
        else:
            response.refresh(code=604, description=10553, error=10553)
        return Response(response.content(), status=state)


class GameStageList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    process_list = ['exist-student']
    format_keys = ['gcid']
    check_list = {
        'gcid': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12051)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            stages = MaoStage.objects.filter(chapter__id=request.data['gcid'])
            serializer = MaoStageSerializer(stages, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=602, description=10554, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class GameStageScore(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    process_list = ['exist-student']
    format_keys = ['gcid', 'student']
    check_list = {
        'gcid': 'id',
        'student': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12052)
        state = status.HTTP_200_OK
        params = request.data
        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            score = MaoScore.objects.filter(stage__chapter__id=request.data['gcid'], user=params['student'])
            serializer = MaoScoreSerializer(score, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(mark=True, code=602, description=10555, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class GameStageRecord(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    process_list = ['exist-student']
    format_keys = ['gsid', 'student']
    check_list = {
        'gsid': 'id',
        'student': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12053)
        state = status.HTTP_200_OK
        params = request.data
        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            recode = MaoRecord.objects.filter(stage=request.data['gsid'], user=params['student']).order_by('judge_time')
            serializer = MaoRecordSerializer(recode, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(mark=True, code=602, description=10556, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class GameStageIsFinished(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    process_list = ['exist-student']
    format_keys = ['gcid', 'student']
    check_list = {
        'gsid': 'id',
        'student': 'id',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12053)
        state = status.HTTP_200_OK
        params = request.data

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        student = detail['student']
        result = mao_chapter_finish(student.user, params['gcid'])
        response.data = result

        return Response(response.content(), status=state)


class GameStageIsUnlock(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    process_list = ['exist-student']
    format_keys = ['gcid', 'student']
    check_list = {
        'gsid': 'id',
        'student': 'id',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12053)
        state = status.HTTP_200_OK
        params = request.data

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        student = detail['student']
        result = mao_chapter_unlock(student.user, params['gcid'])
        response.data = result

        return Response(response.content(), status=state)

