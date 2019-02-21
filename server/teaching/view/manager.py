import copy
import json

from django.contrib.auth.models import User
from django.db.models import Q

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response

from teaching.models import *
from kudingmao.models import JudgeRecord as MaoCode, GameStage as MaoGameStage, UserStagesStatistic as MaoScore, Chapter as MaoGameChapter
from teaching.serializers import *

from teaching.unit.permission import ManagerPermission
from teaching.response_content import ResponseContent

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from teaching.unit.ValidView import ValidApiView

from kudingmao.stage_controller import unlockNewChapter as mao_open_chapter, \
    isChapterUnlocked as mao_chapter_unlock

#课程 Cls
class ClassList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12008)
        state = status.HTTP_200_OK

        try:
            organization = Cls.objects.all()
            serializer = ClassSerializer(organization, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=602, description=10506, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class AddClass(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    # process_list = ['exist-teacher', 'exist-school']
    process_list = ['exist-teacher',]
    format_keys = ['name', 'teacher', 'launch', 'deadline']
    check_list = {
        'name': 'appellation',
        'teacher': 'id',
        # 'school': 'id',
        'launch': 'iso',
        'deadline': 'iso'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12009)
        state = status.HTTP_200_OK
        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = ClassSerializer(data=self.formatData(request), partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=601, description=10507, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)

    def formatData(self, request):
        result = {}
        for key in request.data:
            result[key] = request.data[key]
        result['creator'] = request.user.id
        return result

    def extra(self, request, detail):
        params = request.data
        response = ResponseContent(code=401, description=10552, error=10552)
        try:
            classes = Cls.objects.filter(
                name=params['name'],
                teacher=params['teacher'],
                start_time=params['launch'],
                end_time=params['deadline']
            )
            if not classes.exists():
                response = True
        except Exception as e:
            return ResponseContent(code=602, description=10507, error=e.__str__())

        return response


class UpdateClass(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    # process_list = ['exist-teacher', 'exist-class', 'exist-school']
    process_list = ['exist-teacher', 'exist-class']
    format_keys = ['oid']
    check_list = {
        'oid': 'id',
        'name': 'appellation',
        'tid': 'id',
        # 'school': 'id',
        'launch': 'iso',
        'deadline': 'iso',
        'enable': 'range2'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12010)
        state = status.HTTP_200_OK
        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = ClassSerializer(detail['class'], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=601, description=10508, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


#班级课程关系  ClsCourse
class PlanList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-class', ]
    format_keys = ['oid']
    check_list = {
        'oid': 'id',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12011)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            plan = ClsCourse.objects.filter(cls=request.data['oid'])
            serializer = PlanSerializer(plan, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=602, description=10509, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class AddPlan(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    # process_list = ['exist-class', 'exist-school', 'exist-course']
    process_list = ['exist-class', 'exist-course']
    format_keys = ['oid', 'cid', 'launch', 'deadline', ]
    check_list = {
        'oid': 'id',
        'cid': 'id',
        # 'school': 'id',
        'launch': 'iso',
        'deadline': 'iso',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12012)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = PlanSerializer(data=self.formatData(request), partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=604, description=10510, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)

    def formatData(self, request):
        result = {}
        for key in request.data:
            result[key] = request.data[key]
        result['creator'] = request.user.id
        return result

    def extra(self, request, detail):
        params = request.data
        response = ResponseContent(code=401, description=10138, error=10138)

        try:
            plan = ClsCourse.objects.filter(cls=params['oid'], course=params['cid'])
            if not plan.exists():
                response = True
        except Exception as e:
            return ResponseContent(code=602, description=10510, error=e.__str__())

        return response

class UpdatePlan(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    # process_list = ['exist-class', 'exist-school', 'exist-course']
    process_list = ['exist-class', 'exist-course', 'exist-plan']
    format_keys = ['pid']
    check_list = {
        'pid': 'id',
        # 'oid': 'id',
        'cid': 'id',
        # 'school': 'id',
        'launch': 'iso',
        'deadline': 'iso',
        'enable': 'range2'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12013)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = PlanSerializer(detail['plan'], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=604, description=10511, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)

    def extra(self, request, detail):
        response = True
        plan = detail['plan']
        params = request.data

        try:
            if 'cid' in params:
                plan = ClsCourse.objects.filter(cls=plan.cls, course=params['cid'])
                if plan.exists():
                    response = ResponseContent(code=401, description=10138, error=10138)
        except Exception as e:
            return ResponseContent(code=602, description=10511, error=e.__str__())

        # if 'cid' in params and 'oid' in params:
        #     response = ResponseContent(code=401, description=10139, error=10139)

        # if 'oid' in params and ClsCourse.objects.filter(cls=params['oid'], course=plan.course).exists():
        #     response = ResponseContent(code=401, description=10138, error=10138)

        # if 'cid' in params and ClsCourse.objects.filter(cls=plan.cls, course=params['cid']).exists():
        #     response = ResponseContent(code=401, description=10138, error=10138)

        return response



# 班级学生 ClsStudent
class EnrollList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-class', ]
    format_keys = ['oid']
    check_list = {
        'oid': 'id',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12014)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            enroll = ClsStudent.objects.filter(cls=request.data['oid'])
            serializer = EnrollSerializer(enroll, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10513, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class AddEnroll(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-class',]
    format_keys = ['oid', ]
    check_list = {
        'oid': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12015)
        state = status.HTTP_200_OK
        params = request.data

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)


        extra = detail['extra']
        failer = 0
        successer = 0

        for sid in extra['students']:
            serializer = EnrollSerializer(data={
                'cls': params['oid'],
                'creater': request.user.id,
                'student': sid,
                'status': 1,
            }, partial=True)
            if serializer.is_valid():
                serializer.save()
                successer += 1
                print(successer)
            else:
                failer += 1

        extra['fail'] = failer
        extra['success'] = successer
        del extra['students']

        response.data = extra

        return Response(response.content(), status=state)

    def formatData(self, request):
        result = {}
        for key in request.data:
            result[key] = request.data[key]
        result['creator'] = request.user.id
        return result

    def extra(self, request, detail):
        response = True
        params = request.data

        student = json.loads(params['student'])

        if not isinstance(student, list):
            return ResponseContent(code=401, description=10154, error=10154)

        used = 0
        errorer = 0
        students = []
        try:
            for sid in student:
                user = User.objects.filter(id=sid)
                if user.exists() and hasattr(user[0], 'userteachingprofile') and user[0].userteachingprofile.role == 0:
                    enroll = ClsStudent.objects.filter(cls=params['oid'], student=sid)
                    if enroll.exists():
                        used += 1
                    else:
                        students.append(sid)
                else:
                    errorer += 1

            response = {
                'used': used,
                'error': errorer,
                'students': tuple(students),
            }
        except Exception as e:
            return ResponseContent(code=602, description=10513, error=e.__str__())

        return response


class UpdateEnroll(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-class', 'exist-student', 'exist-enroll']
    format_keys = ['eid']
    check_list = {
        'eid': 'id',
        'oid': 'id',
        'student': 'id',
        'status': 'range4',
        'enable': 'range2'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12016)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = EnrollSerializer(detail['enroll'], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=604, description=10514, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)

    def extra(self, request, detail):
        response = True
        params = request.data
        enroll = detail['enroll']

        if 'student' in params and 'oid' in params:
            response = ResponseContent(code=401, description=10141, error=10141)

        # if 'oid' in params and ClsStudent.objects.filter(cls=params['cid'], student=enroll.student).exists():
        #     response = ResponseContent(code=401, description=10140, error=10140)


        try:
            if 'student' in params and ClsStudent.objects.filter(cls=enroll.cls, student=params['student']).exists():
                response = ResponseContent(code=401, description=10140, error=10140)
        except Exception as e:
            return ResponseContent(code=602, description=10514, error=e.__str__())

        return response


#课程 Course
class CourseList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12017)
        state = status.HTTP_200_OK
        try:
            course = Course.objects.all()
            serializer = CourseSerializer(course, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10515, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class AddCourse(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    format_keys = ['name', 'language',]
    check_list = {
        'name': 'appellation',
        'language': 'range5',
        'grade': 'range5',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12018)
        state = status.HTTP_200_OK

        serializer = CourseSerializer(data=self.formatData(request), partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=604, description=10516, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)

    def formatData(self, request):
        result = {}
        for key in request.data:
            result[key] = request.data[key]
        result['creator'] = request.user.id
        return result


class UpdateCourse(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-course',]
    format_keys = ['cid']
    check_list = {
        'cid': 'id',
        'name': 'appellation',
        'language': 'range5',
        'enable': 'range2',
        'grade': 'range5',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12019)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = CourseSerializer(detail['course'], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=604, description=10517, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


#课时 Lesson
class LessonList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-course', ]
    format_keys = ['cid']
    check_list = {
        'cid': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12020)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            lessons = Lesson.objects.filter(course=request.data['cid'])
            serializer = LessonSerializer(lessons, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10518, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class AddLesson(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-course', ]
    format_keys = ['cid', 'name']
    check_list = {
        'name': 'appellation',
        'cid': 'id',
        'enable': 'range2'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12021)
        state = status.HTTP_200_OK
        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = LessonSerializer(data=self.formatData(request), partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=11001, description=10519, error=serializer.errors)
            state = status.HTTP_501_NOT_IMPLEMENTED

        return Response(response.content(), status=state)

    def formatData(self, request):
        result = {}
        for key in request.data:
            result[key] = request.data[key]
        result['creator'] = request.user.id
        return result


class UpdateLesson(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-lesson', 'exist-course', ]
    format_keys = ['lid']
    check_list = {
        'lid': 'id',
        'name': 'appellation',
        'cid': 'id',
        'enable': 'range2'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12022)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = LessonSerializer(detail['lesson'], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=11001, description=10520, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


# 课程表 Curriculum
class CurriculumList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-class', 'exist-course', ]
    format_keys = ['oid', 'cid']
    check_list = {
        'oid': 'id',
        'cid': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12023)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            curriculum = Curriculum.objects.filter(cls=request.data['oid'], lesson__course=request.data['cid'])
            serializer = CurriculumSerializer(curriculum, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10521, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class AddCurriculum(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    # process_list = ['exist-lesson', 'exist-class', 'exist-school']
    process_list = ['exist-lesson', 'exist-class',]
    format_keys = ['oid', 'lid', 'launch', 'deadline',]
    check_list = {
        'oid': 'id',
        'lid': 'id',
        # 'school': 'id',
        'launch': 'iso',
        'deadline': 'iso',
        # 'classroom': 'appellation'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12024)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = CurriculumSerializer(data=self.formatData(request), partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=11001, description=10522, error=serializer.errors)
            state = status.HTTP_501_NOT_IMPLEMENTED

        return Response(response.content(), status=state)

    def formatData(self, request):
        result = {}
        for key in request.data:
            result[key] = request.data[key]
        result['creator'] = request.user.id
        return result

    def extra(self, request, detail):
        response = True
        params = request.data

        try:
            curriculum = Curriculum.objects.filter(cls=params['oid'], lesson=params['lid'])
            if curriculum.exists():
                response = ResponseContent(code=401, description=10142, error=10142)
        except Exception as e:
            return ResponseContent(code=602, description=10522, error=e.__str__())

        return response


class UpdateCurriculum(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    # process_list = ['exist-lesson', 'exist-school', 'exist-curriculum']
    process_list = ['exist-lesson', 'exist-curriculum']
    format_keys = ['curid']
    check_list = {
        'curid': 'id',
        'lid': 'id',
        # 'school': 'id',
        'classroom': 'appellation',
        'launch': 'iso',
        'deadline': 'iso',
        'enable': 'range2'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12025)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = CurriculumSerializer(detail['curriculum'], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=604, description=10523, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)

    def extra(self, request, detail):
        response = True
        params = request.data
        curriculum = detail['curriculum']

        try:
            if 'lid' in params and Curriculum.objects.filter(cls=curriculum.cls, lesson=params['lid']).exists():
                response = ResponseContent(code=401, description=10142, error=10142)
        except Exception as e:
            return ResponseContent(code=602, description=10523, error=e.__str__())

        return response


#学生 Student
class StudentList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    check_list = {
        'keywords': 'appellation'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12026)
        state = status.HTTP_200_OK
        try:
            students = None
            if 'keywords' in request.data:
                students = UserTeachingProfile.objects.filter(role=0, name__contains=request.data['keywords'])
            else:
                students = UserTeachingProfile.objects.filter(role=0)
            serializer = UserProfileSerializer(students, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10524, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class AddStudent(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['no-exist-account']
    format_keys = ['account', 'password', 'name', 'sex', 'grade',]
    check_list = {
        'account': 'account',
        'password': 'password',
        'name': 'name',
        'sex': 'range2',
        'phone': 'phone',
        # 'school': 'id',
        'grade': 'range13'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=601, token=request.auth, description=10525)
        state = status.HTTP_500_INTERNAL_SERVER_ERROR

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        params = request.data
        serializer = UserSerializer(data={
            'username': params['account'],
            'password': params['password'],
            'first_name': params['name'][0:1],
            'last_name': params['name'][1:]
        }, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = self.formatData(request, serializer.data['uid'])
            serializer = UserProfileSerializer(data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response.refresh(code=200, description=12027, data=serializer.data)
                state = status.HTTP_200_OK
            else:
                response.error = serializer.errors
        else:
            response.error = serializer.errors

        return Response(response.content(), status=state)

    def formatData(self, request, uid):
        result = {}
        for key in request.data:
            result[key] = request.data[key]
        result['user'] = uid
        result['role'] = 0
        result['creator'] = request.user.id
        return result


class UpdateStudent(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-student', 'bind-phone']
    format_keys = ['sid']
    check_list = {
        'sid': 'id',
        'phone': 'phone',
        'name': 'name',
        'sex': 'range2',
        'role': 'role',
        # 'school': 'id',
        'grade': 'range13',
        'enable': 'range2',
        'enroll': 'range2'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12028)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        student = detail['student']

        if 'name' in request.data or 'password' in request.data:
            user_data = {}
            if 'name' in request.data:
                user_data['first_name'] = request.data['name'][0:1]
                user_data['last_name'] = request.data['name'][1:]
            if 'password' in request.data:
                user_data['password'] = request.data['password']

            serializer = UserSerializer(student.user, data=user_data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                response.refresh(code=602, description=10548, error=serializer.errors)
                state = status.HTTP_500_INTERNAL_SERVER_ERROR

        serializer = UserProfileSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=602, description=10526, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)



#教师 Teacher
class TeacherList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]


    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12029)
        state = status.HTTP_200_OK
        try:
            teachers = UserTeachingProfile.objects.exclude(role=0)
            serializer = UserProfileSerializer(teachers, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10527, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class AddTeacher(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['no-exist-account']
    format_keys = ['account', 'password', 'name', 'sex', 'role',]
    check_list = {
        'account': 'account',
        'password': 'password',
        'name': 'name',
        'sex': 'range2',
        'role': 'role',
        'phone': 'phone',
        # 'school': 'id',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=601, token=request.auth, description=10528)
        state = status.HTTP_500_INTERNAL_SERVER_ERROR

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        params = request.data

        serializer = UserSerializer(data={
            'username': params['account'],
            'password': params['password'],
            'first_name': params['name'][0:1],
            'last_name': params['name'][1:]
        }, partial=True)

        if serializer.is_valid():
            serializer.save()
            data = self.formatData(request, serializer.data['uid'])
            serializer = UserProfileSerializer(data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response.refresh(code=200, description=12030, data=serializer.data)
                state = status.HTTP_200_OK
            else:
                response.error = serializer.errors
        else:
            response.error = serializer.errors

        return Response(response.content(), status=state)

    def formatData(self, request, uid):
        result = {}
        for key in request.data:
            result[key] = request.data[key]
        result['user'] = uid
        result['creator'] = request.user.id
        return result


class UpdateTeacher(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-teacher', 'bind-phone']
    format_keys = ['tid']
    check_list = {
        'tid': 'id',
        'phone': 'phone',
        'password': 'password',
        'name': 'name',
        'sex': 'range2',
        'role': 'role',
        # 'school': 'id',
        'enable': 'range2'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12031)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        teacher = detail['teacher']

        if 'name' in request.data or 'password' in request.data:
            user_data = {}
            if 'name' in request.data:
                user_data['first_name'] = request.data['name'][0:1]
                user_data['last_name'] = request.data['name'][1:]
            if 'password' in request.data:
                user_data['password'] = request.data['password']

            serializer = UserSerializer(teacher.user, data=user_data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                response.refresh(code=602, description=10548, error=serializer.errors)
                state = status.HTTP_500_INTERNAL_SERVER_ERROR

        serializer = UserProfileSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=11001, description=10529, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)



#作业 Homework
class HomeworkList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-class', 'exist-lesson']
    check_list = {
        'oid': 'id',
        'lid': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12032)
        state = status.HTTP_200_OK
        params = request.data

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            condition = Q(id__gt=0)
            if 'oid' in params:
                condition = condition & Q(curriculum__cls=params['oid'])
            if 'lid' in params:
                condition = condition & Q(curriculum__lesson=params['lid'])

            homework = Homework.objects.filter(condition)
            serializer = HomeworkSerializer(homework, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10530, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class AddHomework(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-curriculum',]
    format_keys = ['curid', 'task', 'launch', 'deadline', 'name']
    check_list = {
        'curid': 'id',
        'launch': 'iso',
        'deadline': 'iso',
        'task': 'equal1',
        'name': 'appellation'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12033)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = HomeworkSerializer(data=self.formatData(request), partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer = CurriculumSerializer(detail['curriculum'], data=self.formatData(request), partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                response.refresh(code=11001, description=11001, error=serializer.errors)
                state = status.HTTP_501_NOT_IMPLEMENTED
        else:
            response.refresh(code=11001, description=10531, error=serializer.errors)
            state = status.HTTP_501_NOT_IMPLEMENTED

        return Response(response.content(), status=state)


    def formatData(self, request):
        result = {}
        for key in request.data:
            result[key] = request.data[key]
        result['creator'] = request.user.id
        return result


class UpdateHomework(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-homework', ]
    format_keys = ['hid']
    check_list = {
        'name': 'appellation',
        'launch': 'iso',
        'deadline': 'iso',
        'stop': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12034)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = HomeworkSerializer(detail['homework'], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=11001, description=10532, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)



#作业内容
class QuestionList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-homework', 'exist-class', 'exist-lesson', ]
    check_list = {
        'hid': 'id',
        'oid': 'id',
        'lid': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12035)
        state = status.HTTP_200_OK
        params = request.data

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            question = []
            if 'hid' in params:
                question = HomeworkDetail.objects.filter(homework=params['hid']).order_by('idx')
            elif 'oid' in params and 'lid' in params:
                question = HomeworkDetail.objects.filter(
                    homework__curriculum__cls=params['oid'],
                    homework__curriculum__lesson=params['lid'],
                ).order_by('idx')
            serializer = QuestionSerializer(question, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10533, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class AddQuestion(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-homework', ]
    format_keys = ['hid', 'gametype', 'gcid', 'idx']
    check_list = {
        'hid': 'id',
        'gcid': 'id',
        # 'gsid': 'id',
        'idx': 'range21',
        'gametype': 'range2',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12036)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)


        serializer = QuestionSerializer(data=self.formatData(request), partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=11001, description=10534, error=serializer.errors)
            state = status.HTTP_501_NOT_IMPLEMENTED

        return Response(response.content(), status=state)

    def formatData(self, request):
        result = {}
        for key in request.data:
            result[key] = request.data[key]
        result['creator'] = request.user.id
        return result

    def extra(self, request, detail):
        response = True
        params = request.data


        try:
            question = HomeworkDetail.objects.filter(
                homework=params['hid'],
                gametype=params['gametype'],
                gcid=params['gcid'],
                # gsid=params['gsid']
            )
            if question.exists():
                response = ResponseContent(code=401, description=10143, error=10143)

            question = HomeworkDetail.objects.filter(
                homework=params['hid'],
                idx=params['idx']
            )

            if question.exists():
                response = ResponseContent(code=401, description=10600, error=10600)
        except Exception as e:
            return ResponseContent(code=602, description=10534, error=e.__str__())

        return response



class UpdateQuestion(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-question', ]
    format_keys = ['qid']
    check_list = {
        'qid': 'id',
        # 'hid': 'id',
        'gcid': 'id',
        'gsid': 'id',
        'idx': 'range21',
        'gametype': 'range2',
        'enable': 'range2'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(
            code=200, token=request.auth, description=12037)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = QuestionSerializer(detail['question'], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=11001, description=10535, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)

    def extra(self, request, detail):
        response = True
        params = request.data

        question = detail['question']
        homework = question.homework
        gametype = question.gametype
        gcid = question.gcid
        gsid = question.gsid
        idx = question.idx


        if 'gametype' in params:
            gametype = params['gametype']
        if 'gcid' in params:
            gcid = params['gcid']
        # if 'gsid' in params:
        #     gsid = params['gsid']
        if 'idx' in params:
            idx = params['idx']


        try:
            # if 'gametype' in params or 'gcid' in params or 'gsid' in params:
            if 'gametype' in params or 'gcid' in params:
                condition = Q(homework=homework) & Q(gametype=gametype) & Q(gcid=gcid)
                question = HomeworkDetail.objects.filter(condition)

                if question.exists():
                    response = ResponseContent(code=401, description=10143, error=10143)

            if 'idx' in params:
                condition = Q(homework=homework) & Q(idx=idx)
                question = HomeworkDetail.objects.filter(condition)

                if question.exists():
                    response = ResponseContent(code=401, description=10600, error=10600)

        except Exception as e:
            return ResponseContent(code=602, description=10535, error=e.__str__())

        return response




# 学校 School
# class AddSchool(ValidApiView):
#     authentication_classes = [JSONWebTokenAuthentication, ]
#     permission_classes = [IsAuthenticated, ManagerPermission, ]
#     format_keys = ['name', 'level']
#     check_list = {
#         'name': 'name',
#         'district': 'appellation',
#         'level': 'range5'
#     }

#     def post(self, request, *args, **kwargs):
#         response = ResponseContent(code=200, token=request.auth, description=12039)
#         state = status.HTTP_200_OK

#         serializer = SchoolSerializer(data=self.formatData(request), partial=True)
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             response.refresh(code=11001, description=10537, error=serializer.errors)
#             state = status.HTTP_501_NOT_IMPLEMENTED

#         return Response(response.content(), status=state)

#     def formatData(self, request):
#         result = {}
#         for key in request.data:
#             result[key] = request.data[key]
#         result['creator'] = request.user.id
#         return result

#     def extra(self, request, detail):
#         response = True
#         params = request.data

#         district = None
#         if 'district' in params:
#             district = params['district']

#         school = School.objects.filter(name=params['name'], district=district, level=params['level'])
#         if school.exists():
#             response = ResponseContent(code=401, description=10144, error=10144)

#         return response



# class UpdateSchool(ValidApiView):
#     authentication_classes = [JSONWebTokenAuthentication, ]
#     permission_classes = [IsAuthenticated, ManagerPermission, ]
#     process_list = ['exist-school']
#     format_keys = ['school']
#     check_list = {
#         'school': 'id',
#         'name': 'name',
#         'district': 'appellation',
#         'level': 'range5',
#         'enable': 'range2'
#     }

#     def post(self, request, *args, **kwargs):
#         response = ResponseContent(code=200, token=request.auth, description=12040)
#         state = status.HTTP_200_OK

#         detail = self.readiness(request)
#         if isinstance(detail, ResponseContent):
#             return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

#         serializer = SchoolSerializer(detail['school'], data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             response.refresh(code=11001, description=10538, error=serializer.errors)
#             state = status.HTTP_500_INTERNAL_SERVER_ERROR

#         return Response(response.content(), status=state)

#     def extra(self, request, detail):
#         response = True
#         params = request.data

#         school = detail['school']
#         if 'name' in params and School.objects.filter(name=params['name'], district=school.district, level=school.level).exists():
#             response = ResponseContent(code=401, description=10144, error=10144)

#         if 'district' in params and School.objects.filter(name=school.name, district=params['district'], level=school.level).exists():
#             response = ResponseContent(code=401, description=10144, error=10144)

#         if 'level' in params and School.objects.filter(name=school.name, district=school.district, level=params['level']).exists():
#             response = ResponseContent(code=401, description=10144, error=10144)

#         return response




# 游戏
class GameChapterList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    format_keys = ['gametype']
    check_list = {
        'gametype': 'range2'
    }


    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12041)
        state = status.HTTP_200_OK
        params = request.data
        try:
            if int(params['gametype']) == 0:
                game_chapter = MaoGameChapter.objects.filter(enable=1)
                serializer = MaoGameChapterSerializer(game_chapter, many=True)
                response.data = serializer.data
            elif params['gametype'] == 1:
                pass
        except Exception as e:
            response.refresh(code=604, description=10539, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class GameStageList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    format_keys = ['gametype', 'gcid']
    check_list = {
        'gametype': 'range2',
        'gcid': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12042)
        state = status.HTTP_200_OK
        params = request.data
        try:
            if int(params['gametype']) == 0:
                game_stage = MaoGameChapter.objects.get(pk=params['gcid']).stages.all()
                serializer = MaoGameStageSerializer(game_stage, many=True)
                response.data = serializer.data
            elif int(params['gametype']) == 1:
                pass
        except Exception as e:
            response.refresh(code=604, description=10540, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)




# 案例
class ExampleList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-lesson']
    format_keys = ['lid', 'enable']
    check_list = {
        'lid': 'id',
        'enable': 'range3'
    }


    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12043)
        state = status.HTTP_200_OK
        params = request.data

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)


        try:
            if int(params['enable']) == 2:
                example = LessonDetail.objects.filter(lesson=params['lid']).order_by('idx')
            else:
                example = LessonDetail.objects.filter(lesson=params['lid'], enable=params['enable']).order_by('idx')
            serializer = ExampleSerializer(example, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10541, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)



class AddExample(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-lesson']
    format_keys = ['lid', 'gametype', 'gcid', 'idx']
    check_list = {
        'lid': 'id',
        'gcid': 'id',
        'idx': 'range21',
        'gametype': 'range2',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12044)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = ExampleSerializer(data=self.formatData(request), partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=11001, description=10542, error=serializer.errors)
            state = status.HTTP_501_NOT_IMPLEMENTED

        return Response(response.content(), status=state)

    def formatData(self, request):
        result = {}
        for key in request.data:
            result[key] = request.data[key]
        result['creator'] = request.user.id
        return result

    def extra(self, request, detail):
        response = True
        params = request.data

        try:
            example = LessonDetail.objects.filter(
                lesson=params['lid'],
                gametype=params['gametype'],
                gcid=params['gcid'],
            )
            if example.exists():
                response = ResponseContent(code=401, description=10145, error=10145)

            example = LessonDetail.objects.filter(
                lesson=params['lid'],
                idx=params['idx']
            )

            if example.exists():
                response = ResponseContent(code=401, description=10600, error=10600)

        except Exception as e:
            return ResponseContent(code=602, description=10542, error=e.__str__())

        return response




class UpdateExample(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-example']
    format_keys = ['leid']
    check_list = {
        'tid': 'id',
        'leid': 'id',
        'gcid': 'id',
        'gsid': 'id',
        'idx': 'range21',
        'gametype': 'range2',
        'enable': 'range2'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12045)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = ExampleSerializer(detail['example'], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=11001, description=10543, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)

    def extra(self, request, detail):
        response = True
        params = request.data

        example = detail['example']
        lesson = example.lesson
        gametype = example.gametype
        gcid = example.gcid
        gsid = example.gsid
        idx = example.idx


        if 'gametype' in params:
            gametype = params['gametype']
        if 'gcid' in params:
            gcid = params['gcid']
        # if 'gsid' in params:
        #     gsid = params['gsid']
        if 'idx' in params:
            idx = params['idx']

        try:
            if 'gametype' in params or 'gcid' in params:
                condition = Q(lesson=lesson) & Q(gametype=gametype) & Q(gcid=gcid)
                example = LessonDetail.objects.filter(condition)

                if example.exists():
                    response = ResponseContent(code=401, description=10145, error=10145)

            if 'idx' in params:
                condition = Q(lesson=lesson) & Q(idx=idx)
                example = LessonDetail.objects.filter(condition)

                if example.exists():
                    response = ResponseContent(code=401, description=10600, error=10600)

        except Exception as e:
            return ResponseContent(code=602, description=10542, error=e.__str__())

        return response



# 作业成绩
class ScoreList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-class']
    format_keys = ['gcid', 'oid']
    check_list = {
        'oid': 'id',
        'gcid': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12046)
        state = status.HTTP_200_OK
        params = request.data

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            enroll = ClsStudent.objects.filter(cls=params['oid'])
            score = MaoScore.objects.filter(stage__chapter=params['gcid'])
            stage = MaoGameStage.objects.filter(chapter=params['gcid']).order_by('idx')
            response.data['student'] = EnrollSerializer(enroll, many=True).data
            response.data['score'] = HighScoreSerializer(score, many=True).data
            response.data['stage'] = MaoGameStageSerializer(stage, many=True).data
        except Exception as e:
            response.refresh(code=604, description=10544, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)



# 课时内容成绩
class ExampleScoreList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-class']
    format_keys = ['oid', 'gcid']
    check_list = {
        'oid': 'id',
        'gcid': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12046)
        state = status.HTTP_200_OK
        params = request.data

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            enroll = ClsStudent.objects.filter(cls=params['oid'])
            score = MaoScore.objects.filter(stage__chapter=params['gcid'])
            stage = MaoGameStage.objects.filter(chapter=params['gcid']).order_by('idx')
            response.data['student'] = EnrollSerializer(enroll, many=True).data
            response.data['score'] = HighScoreSerializer(score, many=True).data
            response.data['stage'] = MaoGameStageSerializer(stage, many=True).data
        except Exception as e:
            response.refresh(code=604, description=10544, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)



class AddComment(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-student', 'exist-homework']
    format_keys = ['student', 'hid', 'content']
    check_list = {
        'student': 'id',
        # 'tid': 'id',
        'hid': 'id'
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(
            code=200, token=request.auth, description=12048)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = CommentSerializer(data=self.formatData(request), partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=11001, description=10546, error=serializer.errors)
            state = status.HTTP_501_NOT_IMPLEMENTED

        return Response(response.content(), status=state)

    def formatData(self, request):
        result = {}
        for key in request.data:
            result[key] = request.data[key]
        result['homework'] = request.data['hid']
        return result


class UpdateComment(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission, ]
    process_list = ['exist-comment',]
    format_keys = ['comment', 'content']
    check_list = {
        'comment': 'id',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12049)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = CommentSerializer(detail['comment'], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            response.refresh(code=11001, description=10547, error=serializer.errors)
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class GameStageOpenChapter(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission]
    process_list = ['exist-class']
    format_keys = ['gcid', 'oid']
    check_list = {
        'gsid': 'id',
        'oid': 'id',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12053)
        state = status.HTTP_200_OK
        params = request.data

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            enroll = ClsStudent.objects.filter(cls=params['oid'])
            if enroll.exists():
                for item in enroll:
                    mao_open_chapter(item.student, params['gcid'])
        except Exception as e:
            response.refresh(code=602, description=10512, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        response.data = True

        return Response(response.content(), status=state)


class GameStageIsUnlock(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ManagerPermission]
    process_list = ['exist-class']
    format_keys = ['gcid', 'oid']
    check_list = {
        'gsid': 'id',
        'oid': 'id',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12053)
        state = status.HTTP_200_OK
        params = request.data

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        openStatus = False

        try:
            enroll = ClsStudent.objects.filter(cls=params['oid'])
            if enroll.exists():
                for item in enroll:
                    result = mao_chapter_unlock(item.student, params['gcid'])
                    if result:
                        openStatus = result
        except Exception as e:
            response.refresh(code=602, description=10560, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        response.data = openStatus

        return Response(response.content(), status=state)
