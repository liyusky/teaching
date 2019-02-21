import copy
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response

from teaching.models import *
from kudingmao.models import JudgeRecord as MaoCode, GameStage as MaoGameStage, UserStagesStatistic as MaoScore, Chapter as MaoGameChapter
from teaching.serializers import *

from teaching.unit.permission import TeacherPermission
from teaching.response_content import ResponseContent

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from teaching.unit.ValidView import ValidApiView

from kudingmao.stage_controller import unlockNewChapter as mao_open_chapter, \
    isChapterUnlocked as mao_chapter_unlock

#课程 Cls
class ClassList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]


    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12008)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        print(request.user.id)

        try:
            organization = Cls.objects.filter(clscourse__teacher=request.user.id)
            serializer = ClassSerializer(organization, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=602, description=10506, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


#班级课程关系  ClsCourse
class PlanList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
    process_list = ['exist-class',]
    format_keys = ['oid',]
    check_list = {
        'oid': 'id',
    }

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12011)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        params = request.data

        try:
            plan = ClsCourse.objects.filter(cls=params['oid'], teacher=request.user.id)
            serializer = PlanSerializer(plan, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=602, description=10509, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


# 班级学生 ClsStudent
class EnrollList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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
            enroll = ClsStudent.objects.filter(cls=request.data['oid'], cls__clscourse__teacher=request.user.id)
            serializer = EnrollSerializer(enroll, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10513, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


#课程 Course
class CourseList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]

    def post(self, request, *args, **kwargs):
        response = ResponseContent(code=200, token=request.auth, description=12017)
        state = status.HTTP_200_OK

        detail = self.readiness(request)
        if isinstance(detail, ResponseContent):
            return Response(detail.content(), status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            course = Course.objects.filter(ClsCourseCourse__teacher=request.user.id)
            serializer = CourseSerializer(course, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10515, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


#课时 Lesson
class LessonList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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
            lessons = Lesson.objects.filter(
                course=request.data['cid'],
                course__ClsCourseCourse__teacher=request.user.id
            )
            serializer = LessonSerializer(lessons, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10518, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)



# 课程表 Curriculum
class CurriculumList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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

        params = request.data

        try:
            curriculum = Curriculum.objects.filter(
                cls=params['oid'],
                lesson__course=params['cid'],
                lesson__course__ClsCourseCourse__teacher=request.user.id
            )
            serializer = CurriculumSerializer(curriculum, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10521, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


    def extra(self, request, detail):
        response = True
        params = request.data

        try:
            courses = ClsCourse.objects.filter(
                cls=params['oid'],
                course=params['cid'],
                teacher=request.user.id
            )
            if not courses.exists():
                return ResponseContent(code=401, description=10601, error=10601)
        except Exception as e:
            return ResponseContent(code=602, description=10559, error=e.__str__())

        return response



class AddCurriculum(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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
        params = request.data

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
        params = request.data

        try:
            curriculum = Curriculum.objects.filter(cls=params['oid'], lesson=params['lid'])
            if curriculum.exists():
                return ResponseContent(code=401, token=request.auth, description=10142, error=10142)

            courses = ClsCourse.objects.filter(
                cls=params['oid'],
                course__LessonCourse=params['lid'],
                teacher=request.user.id
            )
            if not courses.exists():
                return ResponseContent(code=401, description=10601, error=10601)
        except Exception as e:
            return ResponseContent(code=604, description=10522, error=e.__str__())

        return True



class UpdateCurriculum(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
    # process_list = ['exist-lesson', 'exist-school', 'exist-curriculum']
    process_list = ['exist-lesson', 'exist-curriculum']
    format_keys = ['curid']
    check_list = {
        'curid': 'id',
        'lid': 'id',
        # 'school': 'id',
        # 'classroom': 'appellation',
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
            if 'lid' in params:
                curri = Curriculum.objects.filter(cls=curriculum.cls, lesson=params['lid'])

                if curri.exists():
                    return ResponseContent(code=401, token=request.auth, description=10142, error=10142)

                courses = ClsCourse.objects.filter(
                    cls=params['oid'],
                    course__LessonCourse=params['lid'],
                    teacher=request.user.id
                )
                if not courses.exists():
                    return ResponseContent(code=401, token=request.auth, description=10601, error=10601)

        except Exception as e:
            return ResponseContent(code=604, token=request.auth, description=10523, error=e.__str__())

        return response



#作业 Homework
class HomeworkList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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
            condition = Q(curriculum__lesson__course__ClsCourseCourse__teacher=request.user.id)
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
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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

    def extra(self, request, detail):
        response = True
        params = request.data

        try:
            curriculum = Curriculum.objects.filter(
                id=params['curid'],
                lesson__course__ClsCourseCourse__teacher=request.user.id
            )
            if not curriculum.exists():
                return ResponseContent(code=401, token=request.auth, description=10601, error=10601)
        except Exception as e:
            return ResponseContent(code=604, token=request.auth, description=10531, error=e.__str__())

        return response



class UpdateHomework(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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


    def extra(self, request, detail):
        response = True
        params = request.data

        try:
            homework = Homework.objects.filter(
                id=params['hid'],
                curriculum__lesson__course__ClsCourseCourse__teacher=request.user.id
            )
            if not homework.exists():
                return ResponseContent(code=401, token=request.auth, description=10601, error=10601)
        except Exception as e:
            return ResponseContent(code=604, token=request.auth, description=10532, error=e.__str__())

        return response



#作业内容
class QuestionList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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
                question = HomeworkDetail.objects.filter(
                    homework=params['hid'],
                    homework__curriculum__lesson__course__ClsCourseCourse__teacher=request.user.id,
                ).order_by('idx')
            elif 'oid' in params and 'lid' in params:
                question = HomeworkDetail.objects.filter(
                    homework__curriculum__cls=params['oid'],
                    homework__curriculum__lesson=params['lid'],
                    homework__curriculum__lesson__course__ClsCourseCourse__teacher=request.user.id,
                ).order_by('idx')
            serializer = QuestionSerializer(question, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10533, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


class AddQuestion(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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
                homework__curriculum__lesson__course__ClsCourseCourse__teacher=request.user.id
            )
            if not question.exists():
                return ResponseContent(code=401, token=request.auth, description=10602, error=10602)

            question = HomeworkDetail.objects.filter(
                homework=params['hid'],
                gametype=params['gametype'],
                gcid=params['gcid'],
                # gsid=params['gsid']
            )
            if question.exists():
                return ResponseContent(code=401, token=request.auth, description=10143, error=10143)

            question = HomeworkDetail.objects.filter(
                homework=params['hid'],
                idx=params['idx']
            )
            if question.exists():
                return ResponseContent(code=401, token=request.auth, description=10600, error=10600)
        except Exception as e:
            return ResponseContent(code=602, description=10542, error=e.__str__())

        return response



class UpdateQuestion(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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
        response = ResponseContent(code=200, token=request.auth, description=12037)
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
            question = HomeworkDetail.objects.filter(
                id=params['qid'],
                homework__curriculum__lesson__course__ClsCourseCourse__teacher=request.user.id
            )

            if not question.exists():
                return ResponseContent(code=401, token=request.auth, description=10602, error=10602)

            # if 'gametype' in params or 'gcid' in params or 'gsid' in params:
            if 'gametype' in params or 'gcid' in params:
                condition = Q(homework=homework) & Q(gametype=gametype) & Q(gcid=gcid)
                question = HomeworkDetail.objects.filter(condition)

                if question.exists():
                    return ResponseContent(code=401, token=request.auth, description=10143, error=10143)

            if 'idx' in params:
                condition = Q(homework=homework) & Q(idx=idx)
                question = HomeworkDetail.objects.filter(condition)

                if question.exists():
                    return ResponseContent(code=401, token=request.auth, description=10600, error=10600)
        except Exception as e:
            return ResponseContent(code=602, description=10542, error=e.__str__())



# 游戏
class GameChapterList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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


# 案例
class ExampleList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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
                example = LessonDetail.objects.filter(
                    lesson=params['lid'],
                    lesson__course__ClsCourseCourse__teacher=request.user.id,
                ).order_by('idx')
            else:
                example = LessonDetail.objects.filter(
                    lesson=params['lid'],
                    enable=params['enable'],
                    lesson__course__ClsCourseCourse__teacher=request.user.id,
                ).order_by('idx')
            serializer = ExampleSerializer(example, many=True)
            response.data = serializer.data
        except Exception as e:
            response.refresh(code=604, description=10541, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)


# 作业成绩
class ScoreList(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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
            enroll = ClsStudent.objects.filter(
                cls=params['oid'],
                cls__clscourse__teacher=request.user.id,
            )
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
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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
            enroll = ClsStudent.objects.filter(
                cls=params['oid'],
                cls__clscourse__teacher=request.user.id,
            )
            score = MaoScore.objects.filter(stage__chapter=params['gcid'])
            stage = MaoGameStage.objects.filter(chapter=params['gcid']).order_by('idx')
            response.data['student'] = EnrollSerializer(enroll, many=True).data
            response.data['score'] = HighScoreSerializer(score, many=True).data
            response.data['stage'] = MaoGameStageSerializer(stage, many=True).data
        except Exception as e:
            response.refresh(code=604, description=10544, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response.content(), status=state)



class GameStageOpenChapter(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission]
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
            enroll = ClsStudent.objects.filter(
                cls=params['oid'],
                cls__clscourse__teacher=request.user.id,
            )
            if enroll.exists():
                for item in enroll:
                    mao_open_chapter(item.student, params['gcid'])
            else:
                response.refresh(code=11001, description=10153, error=10153)
        except Exception as e:
            response.refresh(code=602, description=10560, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        response.data = True

        return Response(response.content(), status=state)


class GameStageIsUnlock(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission]
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
            enroll = ClsStudent.objects.filter(
                cls=params['oid'],
                cls__clscourse__teacher=request.user.id,
            )
            if enroll.exists():
                for item in enroll:
                    result = mao_chapter_unlock(item.student, params['gcid'])
                    if result:
                        openStatus = result
            else:
                response.refresh(code=11001, description=10153, error=10153)
        except Exception as e:
            response.refresh(code=602, description=10560, error=e.__str__())
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        response.data = openStatus

        return Response(response.content(), status=state)



class AddComment(ValidApiView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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
    permission_classes = [IsAuthenticated, TeacherPermission, ]
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
