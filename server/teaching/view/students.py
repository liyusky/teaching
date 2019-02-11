from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response

from teaching.models import *
from kudingmao.models import JudgeRecord, GameStage as MaoStage, UserStagesStatistic as MaoScore, \
    Chapter as MaoChapter
from teaching.serializers import CourseSerializer, LessonSerializer, ClassSerializer, HomeworkSerializer, ExampleSerializer, \
    QuestionSerializer




from teaching.response_content import ResponseContent
from teaching.unit.permission import StudentPermission
from kudingmao.stage_controller import accessChapter as mao_access_chapter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from teaching.unit.ValidView import ValidApiView


class CourseList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, StudentPermission]

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12017)
        state = status.HTTP_200_OK

        try:
            calss_list = Cls.objects.filter(students=request.user.id, enable=1)
            serializer = ClassSerializer(calss_list, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10515, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class LessonList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, StudentPermission, ]
    process_list = ['exist-course', ]
    format_keys = ['cid']
    check_list = {
        'cid': 'id',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12020)
        state = status.HTTP_200_OK
        detail = self.readiness(request)

        try:
            lessons = Lesson.objects.filter(course=request.data['cid'])
            serializer = LessonSerializer(lessons, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10518, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class HomeworkDetailScoreList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, StudentPermission, ]
    process_list = ['exist-lesson', 'exist-class', ]
    format_keys = ['lid', 'oid']
    check_list = {
        'oid': 'id',
        'lid': 'id',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12032)
        state = status.HTTP_200_OK
        params = request.data
        data = []
        detail = self.readiness(request)

        try:
            question = HomeworkDetail.objects.filter(
                homework__curriculum__cls=params['oid'],
                homework__curriculum__lesson=params['lid'],
            )
            serializer = QuestionSerializer(question, many=True)
            # for item in question:
            #     result = {}
            #     if item.gametype == 0:
            #         score = MaoScore.objects.filter(stage=item.gsid, user=request.user.id)
            #         if score.exists():
            #             score = score.last()
            #             result = {
            #                 'index': item.idx,
            #                 'gcid': item.gcid,
            #                 'game': 0,
            #                 'score': score.high_score,
            #                 'gsid': score.stage.id,
            #                 'stage': score.stage.name,
            #                 'doit': True
            #             }
            #         else:
            #             stage = MaoStage.objects.filter(id=item.gsid)
            #             if stage.exists():
            #                 stage = stage.last()
            #                 result = {
            #                     'index': item.idx,
            #                     'gcid': item.gcid,
            #                     'game': 0,
            #                     'score': 0,
            #                     'gsid': stage.id,
            #                     'stage': stage.name,
            #                     'doit': False,
            #                 }
            #     if item.gametype == 1:
            #         result = {
            #             'game': 1
            #         }

            #     if result:
            #         data.append(result)

            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10533, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class LessonDetailScoreList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, StudentPermission, ]
    process_list = ['exist-lesson']
    format_keys = ['lid']
    check_list = {
        'lid': 'id',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(mark=False, code=200, token=request.auth, description=12017)
        state = status.HTTP_200_OK
        params = request.data
        data = []

        detail = self.readiness(request)
        try:
            example = LessonDetail.objects.filter(lesson=params['lid']).order_by('idx')
            serializer = ExampleSerializer(example, many=True)
            # for item in example:
            #     result = {}
            #     if item.gametype == 0:
            #         score = MaoScore.objects.filter(stage=item.gsid, user=request.user.id).last()
            #         if score:
            #             result = {
            #                 'game': 0,
            #                 'gcid': item.gcid,
            #                 'index': item.idx,
            #                 'score': score.high_score,
            #                 'gsid': score.stage.id,
            #                 'stage': score.stage.name,
            #                 'doit': True
            #             }
            #         else:
            #             stage = MaoStage.objects.filter(id=item.gsid)
            #             if stage.exists():
            #                 stage = stage.last()
            #                 result = {
            #                     'game': 0,
            #                     'gcid': item.gcid,
            #                     'index': item.idx,
            #                     'gsid': stage.id,
            #                     'stage': stage.name,
            #                     'score': 0,
            #                     'doit': False
            #                 }

            #     if item.gametype == 1:
            #         result = {
            #             'game': 1
            #         }
            #     if result:
            #         data.append(result)

            response.data = serializer.data
        except Exception as e:
            response.refresh(mark=True, code=604, description=10515, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)
