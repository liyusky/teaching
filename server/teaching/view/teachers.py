# from django.http import HttpResponse
# from django.db.models.query_utils import Q

# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from teaching.models import *
# from kudingmao.models import JudgeRecord, GameStage, UserStagesStatistic
# from teaching.serializers import GetCourseListSerializer, GetChapterSerializer, \
#     GetHomeworkDetailSerializer, GetClsSerializer, SetCommentSerializer

# from teaching.authentication.teachers import *
# from teaching.response_content import ResponseContent

# class CourseListView(APIView):
#     authentication_classes = [TeacherCourseListAuthentication, ]

#     def post(self, request, *args, **kwargs):
#         response = ResponseContent(mark=False, code=200, token=request.auth.token, description='课程列表获取成功')
#         state = status.HTTP_200_OK
#         try:
#             course = Clscourse.objects.filter(teacher=request.user)
#             serializer = GetCourseListSerializer(course, many=True)
#             response.data = serializer.data
#         except Exception as e:
#             response.refresh(mark=True, code=604, description=604, error=604)
#             state = status.HTTP_500_INTERNAL_SERVER_ERROR

#         return Response(response.content(), status=state)


# class CourseDetailView(APIView):
#     authentication_classes = [TeacherCourseDetailAuthentication, ]

#     def post(self, request, *args, **kwargs):
#         response = ResponseContent(mark=False, code=200, token=request.auth.token, description=20003)
#         state = status.HTTP_200_OK
#         try:
#             detail = CourseDetail.objects.filter(course=request.data['cid'])
#             serializer = GetChapterSerializer(detail, many=True)
#             response.data = serializer.data
#         except Exception as e:
#             response.refresh(mark=True, code=605, description=605, error=e.__str__())
#             state = status.HTTP_500_INTERNAL_SERVER_ERROR

#         return Response(response.content(), status=state)


# class HomeworkReport(APIView):
#     authentication_classes = [TeacherHomeworkReportAuthentication, ]

#     def post(self, request, *args, **kwargs):
#         response = ResponseContent(mark=False, code=200, token=request.auth.token, description=20004)
#         state = status.HTTP_200_OK

#         params = request.data

#         details = HomeworkDetail.objects.filter(homework=params['hid'])
#         serializer = GetHomeworkDetailSerializer(details, many=True)
#         contents = serializer.data

#         organization = Cls.objects.get(id=params['oid'])
#         serializer = GetClsSerializer(organization)
#         sids = serializer.data['sids']

#         students = {}
#         scores = {}
#         for sid in sids:
#             student = User.objects.get(id=sid)
#             students[sid] = student.last_name
#             scores[sid] = []
#             for content in contents:
#                 if content['type'] == 0:
#                     stage = GameStage.objects.get(id=content['gid'])
#                     source = UserStagesStatistic.objects.filter(stage=stage, user=sid).first()
#                     scores[sid].append({
#                         'type': content['type'],
#                         'gid': stage.id,
#                         'title': stage.name,
#                         'score': source.high_score if source else False,
#                     })

#         response.data = {
#             'students': students,
#             'scores': scores
#         }
#         try:
#             pass
#         except Exception as e:
#             response.refresh(mark=True, code=608, error=e.__str__())
#             state = status.HTTP_500_INTERNAL_SERVER_ERROR

#         return Response(response.content(), status=state)


# class CommentView(APIView):
#     authentication_classes = [TeacherCommentAuthentication, ]

#     def post(self, request, *args, **kwargs):
#         response = ResponseContent(mark=False, code=200, token=request.auth.token, description='更新课程评价成功')
#         state = status.HTTP_200_OK

#         params = request.data

#         try:
#             comment = Comment.objects.update_or_create(
#                 homework=params['hid'],
#                 student=params['sid'],
#                 teacher=params['tid'],
#                 defaults={
#                     'comment': params['comment']
#                 }
#             )
#             if not comment:
#                 response.refresh(mark=True, code=608, error=608)
#                 state = status.HTTP_500_INTERNAL_SERVER_ERROR

#         except Exception as e:
#             response.refresh(mark=True, code=608, error=e.__str__())
#             state = status.HTTP_500_INTERNAL_SERVER_ERROR

#         return Response(response, status=status.HTTP_501_NOT_IMPLEMENTED)
