import re
from django.db.models import Q

from rest_framework import exceptions
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.utils import timezone
from teaching.serializers import UserProfileSerializer

from teaching.response_content import ResponseContent
from rest_framework.response import Response
from teaching.captcha import Captcha
from teaching.models import *
from kudingmao.models import GameStage as MaoStage, UserStagesStatistic as MaoScore, JudgeRecord as MaoRecord


class HasParams(object):
    format_keys = {}
    __has_param_result = True

    def has_param(self, params_list):
        lose_list = []
        for key in self.format_keys:
            if not (key in params_list):
                self.__has_param_result = False
                lose_list.append(key)

        if not self.__has_param_result:
            self.__has_param_result = ResponseContent(
                code=401, description=10100, error=lose_list)

        return self.__has_param_result

class FormatParams(object):
    check_list = {}

    def phone(self, phone):
        phone = re.sub(r'\s+', '', phone, count=0)
        if re.match(r'^(?:13|14|15|17|18)[0-9]{9}$', phone):
            return True
        return False

    def password(self, password):
        password = re.sub(r'\s+', '', password, count=0)
        if re.match(r'^\S{6,20}$', password):
            return True
        return False

    def imageCode(self, code):
        code = re.sub(r'\s+', '', code, count=0)
        if re.match(r'^[a-zA-Z0-9]{4}$', code):
            return True
        return False

    def smsCode(self, code):
        code = re.sub(r'\s+', '', code, count=0)
        if re.match(r'^[0-9]{6}$', code):
            return True
        return False

    def name(self, name):
        name = re.sub(r'\s+', '', name, count=0)
        if re.match(r'^[\u4E00-\u9FA5]{2,}(?:·[\u4E00-\u9FA5]{2,5})*', name):
            return True
        return False

    def equal1(self, number):
        if int(number) == 1:
            return True
        return False

    def range2(self, number):
        if int(number) in range(2):
            return True
        return False

    def range3(self, number):
        if int(number) in range(3):
            return True
        return False

    def range4(self, number):
        if int(number) in range(4):
            return True
        return False

    def range5(self, number):
        if int(number) in range(5):
            return True
        return False

    def range21(self, number):
        if int(number) in range(21):
            return True
        return False

    def role(self, number):
        if int(number) in [0, 1, 2, 3, 4, 99]:
            return True
        return False

    def range13(self, number):
        if not (int(number) in range(13)):
            return False
        return True

    def id(self, id):
        if id.isdecimal() and int(id) > 0:
            return True
        return False

    def account(self, account):
        account = re.sub(r'\s+', '', account, count=0)
        if re.match(r'^[A-Za-z0-9_\-]{6,30}', account):
            return True
        return False

    def shortAccount(self, account):
        account = re.sub(r'\s+', '', account, count=0)
        if re.match(r'^[A-Za-z0-9_·@\-]{1,50}', account):
            return True
        return False

    def appellation(self, appellation):
        appellation = re.sub(r'\s+', '', appellation, count=0)

        if re.match(r'[;]+', appellation):
            return False

        if re.match(r'[\S\u4e00-\u9fa5]+', appellation):
            return True
        return False

    def iso(self, date):
        date = re.sub(r'\s+', '', date, count=0)
        if re.match(r'^(?:[1-9]\d{3}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1\d|2[0-8])|(?:0[13-9]|1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[1-9]\d(?:0[48]|[2468][048]|[13579][26])|(?:[2468][048]|[13579][26])00)-02-29)T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d.\d{3}(?:Z|[+-][01]\d:[0-5]\d)$', date):
            return True
        return False

    def match_params(self, params):
        response = True
        for key, value in self.check_list.items():
            if key in params:
                match = getattr(self, value)
                if not match(params[key]):
                    response = ResponseContent(code=401, description=10101, error=key + '不正确')
                    break
        return response

class Exist(object):
    scene = None

    def match_sms_captcha(self, params, scene):
        account = None
        if 'phone' in params:
            account = params['phone']
        elif 'account' in params:
            account = params['account']
        sms_code = params['smsCode']
        response = ResponseContent(code=401, description=10704, error=10704)

        try:
            sms = SMS.objects.filter(phone=account)
            if sms.exists():
                sms = sms.first()
                if sms.used != 0:
                    response.refresh(code=401, description=10700, error=10700)
                if sms.scene != int(scene):
                    response.refresh(code=401, description=10701, error=10701)
                elif datetime.now() - sms.end_time.replace(tzinfo=None) > timedelta(hours=24):
                    response.refresh(code=401, description=10702, error=10702)
                elif sms_code != sms.secret:
                    response.refresh(code=401, description=10703, error=10703)
                else:
                    sms.used = 1
                    sms.save()
                    response = True

        except Exception as e:
            response.refresh(code=602, description=10803, error=e.__str__())

        return response

    def exist_bind_phone(self, request):
        params = request.data
        user = request.user
        response = ResponseContent(code=401, description=10151, error=10151)
        try:
            uid = 0
            if 'sid' in params:
                uid = params['sid']
            elif 'tid' in params:
                uid = params['tid']

            user = User.objects.filter(username=params['phone'])
            profile = UserTeachingProfile.objects.filter(phone=params['phone'])
            if (user.exists() and user.first().id == uid) or (profile.exists() and profile.first().user == uid):
                response = True
            elif not user.exists() and not profile.exists():
                response = True

        except Exception as e:
            response.refresh(code=602, description=10800, error=e.__str__())

        return response

    def match_scene(self, params):
        response = True
        scene = int(params['scene'])
        profile = UserTeachingProfile.objects.filter(phone=params['phone'])

        if scene == 1 and profile.exists():
            response = ResponseContent(code=401, description=10105, error=10105)
        if scene != 1 and (not profile.exists()):
            response = ResponseContent(code=401, description=10104, error=10104)

        return response

    def exist_account(self, params):
        response = ResponseContent(code=401, description=10104, error=10104)
        try:
            user = User.objects.filter(username=params['phone'])

            if user.exists():
                user = user.first()
                if not hasattr(user, 'userteachingprofile'):
                    data = {
                        'user': user.id,
                        'role': 100 if int(user.is_superuser) == 1 else 0,
                        'creator': -1,
                        'name': user.first_name + user.last_name,
                        'enable': 1 if user.is_active else 0
                    }
                    serializer = UserProfileSerializer(data=data, partial=True)
                    if serializer.is_valid():
                        profile = serializer.save()
                        response = (user, profile)
                    else:
                        response = ResponseContent(code=401, description=10147, error=serializer.errors)
                else:
                    serializer = UserProfileSerializer(user.userteachingprofile, data={
                        'role': 100 if int(user.is_superuser) == 1 else user.userteachingprofile.role,
                        'name': user.first_name + user.last_name,
                        'enable': 1 if user.is_active else 0
                    }, partial=True)
                    if serializer.is_valid():
                        profile = serializer.save()
                        response = (user, profile)
                    else:
                        response = ResponseContent(code=401, description=10152, error=serializer.errors)
        except Exception as e:
            response.refresh(code=602, description=10801, error=e.__str__())

        return response

    def exist_not_account(self, params):
        response = ResponseContent(code=401, description=10105, error=10105)

        try:
            user = User.objects.filter(username=params['account'])
            profile = UserTeachingProfile.objects.filter(phone=params['account'])
            if user.exists() or profile.exists():
                response = ResponseContent(code=401, description=10105, error=10105)
            elif not 'phone' in params:
                response = True
            elif 'phone' in params:
                user = User.objects.filter(username=params['phone'])
                profile = UserTeachingProfile.objects.filter(phone=params['phone'])
                if user.exists() or profile.exists():
                    response.refresh(code=401, description=10550, error=10550)
                else:
                    response = True

        except Exception as e:
            response.refresh(code=602, description=10802, error=e.__str__())

        return response

    def exist_student(self, params):
        response = ResponseContent(code=401, description=10106, error=10106)
        try:
            stundent = None
            if 'student' in params:
                stundent = params['student']
            if 'sid' in params:
                stundent = params['sid']

            student = UserTeachingProfile.objects.filter(user=stundent, role=0)
            if student.exists():
                response = student.first()
        except Exception as e:
            response.refresh(code=602, description=10806, error=e.__str__())

        return response

    def exist_user(self, params):
        response = ResponseContent(code=401, description=10104, error=10104)
        try:
            user = User.objects.filter(id=params['user'])
            if user.exists():
                response = user.first()
        except Exception as e:
            response.refresh(code=602, description=10558, error=e.__str__())

        return response




    def exist_teacher(self, params):
        response = ResponseContent(code=401, description=10108, error=10108)
        # manager = UserTeachingProfile.objects.filter(id=params['mid']).exclude(Q(role=0) | Q(role=1) | Q(role=2)).first()
        try:
            teacher = None
            if 'teacher' in params:
                teacher = params['teacher']
            if 'tid' in params:
                teacher = params['tid']

            teacher = UserTeachingProfile.objects.filter(user=teacher).exclude(role=0)
            if teacher.exists():
                response = teacher.first()
        except Exception as e:
            response.refresh(code=602, description=10805, error=e.__str__())

        return response


    # def exist_school(self, params):
    #     response = ResponseContent(code=401, description=10110, error=10110)
    #     try:
    #         school = School.objects.filter(id=params['school'])
    #         if school.exists():
    #             response = school.first()
    #     except Exception as e:
    #         response.refresh(code=602, description=10804, error=e.__str__())

    #     return response

    def match_enable(self, profile, code):
        response = ResponseContent(code=401, description=code, error=code)
        if profile.enable:
            response = True
        return response

    def exist_class(self, params):
        response = ResponseContent(code=401, description=10111, error=10111)
        try:
            organization = Cls.objects.filter(id=params['oid'])
            if organization.exists():
                response = organization.first()
        except Exception as e:
            response.refresh(code=602, description=10807, error=e.__str__())

        return response

    def exist_course(self, params):
        response = ResponseContent(code=401, description=10112, error=10112)
        try:
            course = Course.objects.filter(id=params['cid'])
            if course.exists():
                response = course.first()
        except Exception as e:
            response.refresh(code=602, description=10808, error=e.__str__())

        return response

    def exist_lesson(self, params):
        response = ResponseContent(code=401, description=10113, error=10113)
        try:
            lesson = Lesson.objects.filter(id=params['lid'])
            if lesson.exists():
                response = lesson.first()
        except Exception as e:
            response.refresh(code=602, description=10809, error=e.__str__())
        return response

    def exist_homework(self, params):
        response = ResponseContent(code=401, description=10114, error=10114)
        try:
            homework = Homework.objects.filter(id=params['hid'])
            if homework.exists():
                response = homework.first()
        except Exception as e:
            response.refresh(code=602, description=10810, error=e.__str__())
        return response

    def exist_plan(self, params):
        response = ResponseContent(code=401, description=10115, error=10115)
        try:
            plan = ClsCourse.objects.filter(id=params['pid'])
            if plan.exists():
                response = plan.first()
        except Exception as e:
            response.refresh(code=602, description=10811, error=e.__str__())

        return response

    def exist_enroll(self, params):
        response = ResponseContent(code=401, description=10116, error=10116)
        try:
            enroll = ClsStudent.objects.filter(id=params['eid'])
            if enroll.exists():
                response = enroll.first()
        except Exception as e:
            response.refresh(code=602, description=10812, error=e.__str__())
        return response

    def exist_curriculum(self, params):
        response = ResponseContent(code=401, description=10117, error=10117)
        try:
            curriculum = Curriculum.objects.filter(id=params['curid'])
            if curriculum.exists():
                response = curriculum.first()
        except Exception as e:
            response.refresh(code=602, description=10813, error=e.__str__())

        return response

    def exist_question(self, params):
        response = ResponseContent(code=401, description=10118, error=10118)
        try:
            question = HomeworkDetail.objects.filter(id=params['qid'])
            if question.exists():
                response = question.first()
        except Exception as e:
            response.refresh(code=602, description=10814, error=e.__str__())
        return response

    def exist_example(self, params):
        response = ResponseContent(code=401, description=10119, error=10119)
        try:
            example = LessonDetail.objects.filter(id=params['leid'])
            if example.exists():
                response = example.first()
        except Exception as e:
            response.refresh(code=602, description=10815, error=e.__str__())

        return response

    def exist_comment(self, params):
        response = ResponseContent(code=401, description=10120, error=10120)
        try:
            comment = Comment.objects.filter(id=params['comment'])
            if comment.exists():
                response = comment.first()
        except Exception as e:
            response.refresh(code=602, description=10816, error=e.__str__())
        return response

    def exist_mao_record(self, params):
        response = ResponseContent(code=401, description=10149, error=10149)
        try:
            record = MaoRecord.objects.filter(id=params['mrcid'])
            if record.exists():
                response = record.first()
        except Exception as e:
            response.refresh(code=602, description=10817, error=e.__str__())
        return response

    def refresh_login(self, request, profile):
        response = True
        try:
            profile = UserTeachingProfile.objects.filter(id=profile.id).update(
                login_time=timezone.now(),
                ip=request.META.get('REMOTE_ADDR')
            )
        except Exception as e:
            response = ResponseContent(code=602, description=10816, error=e.__str__())
            return response


class CheckImageCode(object):
    def match_image_captcha(self, request, params):
        key = request.session.session_key

        _code = request.session.get(key) or ''
        request.session[key] = ''

        response = True

        if not (_code.lower() == str(params['imageCode']).lower()):
            response = ResponseContent(code=401, description=10102, error=10102)

        return response


class ValidApiView(APIView, HasParams, FormatParams, Exist, CheckImageCode):

    process_list = []
    detail = {}

    def readiness(self, request):
        params = request.data
        user, profile = (True, True)

        if not 'no-jwt' in self.process_list:
            user = request.user
            profile = user.userteachingprofile

        has_param = self.has_param(params)
        if isinstance(has_param, ResponseContent):
            has_param.refresh(token=request.auth)
            return has_param

        match_params = self.match_params(params)
        if isinstance(match_params, ResponseContent):
            match_params.refresh(token=request.auth)
            return match_params

        if 'image-code' in self.process_list:
            print('---------------image-code-------------------')
            image_code = self.match_image_captcha(request, params)
            if isinstance(image_code, ResponseContent):
                image_code.refresh(token=request.auth)
                return image_code

        if 'scene' in self.process_list:
            print('---------------scene-------------------')
            scene = self.match_scene(params)
            if isinstance(scene, ResponseContent):
                scene.refresh(token=request.auth)
                return scene

        if 'exist-account' in self.process_list and (not 'scene' in params or int(params['scene']) != 1):
            print('---------------exist-account-------------------')
            result = self.exist_account(params)

            if isinstance(result, ResponseContent):
                result.refresh(token=request.auth)
                return result

            if 'current-account' in self.process_list:
                user, profile = result
                if not 'enable' in params:
                    enable = self.match_enable(profile, 10121)
                    if isinstance(enable, ResponseContent):
                        enable.refresh(token=request.auth)
                        return enable

        if 'no-exist-account' in self.process_list and (not 'scene' in params or int(params['scene']) == 1):
            print('---------------no-exist-account-------------------')
            result = self.exist_not_account(params)
            if isinstance(result, ResponseContent):
                result.refresh(token=request.auth)
                return result


        if 'sms-code' in self.process_list:
            print('---------------smsCode-------------------')
            sms = self.match_sms_captcha(params, self.scene)
            if isinstance(sms, ResponseContent):
                sms.refresh(token=request.auth)
                return sms

        # if 'school' in params and 'exist-school' in self.process_list:
        #     print('---------------school-------------------')
        #     school = self.exist_school(params)
        #     self.detail['school'] = school
        #     if isinstance(school, ResponseContent):
        #         school.refresh(token=request.auth)
        #         return school

        #     if not 'enable' in params:
        #         enable = self.match_enable(school, 10123)
        #         if isinstance(enable, ResponseContent):
        #             enable.refresh(token=request.auth)
        #             return enable

        if 'user' in params and 'exist-user' in self.process_list:
            print('---------------user---------------')
            account = self.exist_user(params)
            self.detail['account'] = account
            if isinstance(account, ResponseContent):
                account.refresh(token=request.auth)
                return account

        if ('teacher' in params or 'tid' in params) and 'exist-teacher' in self.process_list:
            print('---------------teacher---------------')
            teacher = self.exist_teacher(params)
            self.detail['teacher'] = teacher
            if isinstance(teacher, ResponseContent):
                teacher.refresh(token=request.auth)
                return teacher

            if not 'enable' in params:
                enable = self.match_enable(teacher, 10124)
                if isinstance(enable, ResponseContent):
                    enable.refresh(token=request.auth)
                    return enable

        if ('student' in params or 'sid' in params) and 'exist-student' in self.process_list:
            print('---------------student-------------------')
            student = self.exist_student(params)

            self.detail['student'] = student

            if isinstance(student, ResponseContent):
                student.refresh(token=request.auth)
                return student

            if not 'enable' in params:
                enable = self.match_enable(student, 10125)
                if isinstance(enable, ResponseContent):
                    enable.refresh(token=request.auth)
                    return enable

        if 'phone' in params and 'bind-phone' in self.process_list:
            print('---------------bind-phone-------------------')
            phone = self.exist_bind_phone(request)

            if isinstance(phone, ResponseContent):
                phone.refresh(token=request.auth)
                return phone

        if 'oid' in params and 'exist-class' in self.process_list:
            print('---------------exist-class-------------------')
            organization = self.exist_class(params)
            self.detail['class'] = organization
            if isinstance(organization, ResponseContent):
                organization.refresh(token=request.auth)
                return organization

            if not 'enable' in params:
                enable = self.match_enable(organization, 10127)
                if isinstance(enable, ResponseContent):
                    enable.refresh(token=request.auth)
                    return enable

        if 'cid' in params and 'exist-course' in self.process_list:
            print('---------------exist-course-------------------')
            course = self.exist_course(params)
            self.detail['course'] = course
            if isinstance(course, ResponseContent):
                course.refresh(token=request.auth)
                return course

            if not 'enable' in params:
                enable = self.match_enable(course, 10128)
                if isinstance(enable, ResponseContent):
                    enable.refresh(token=request.auth)
                    return enable

        if 'pid' in params and 'exist-plan' in self.process_list:
            print('---------------exist-plan-------------------')
            plan = self.exist_plan(params)
            self.detail['plan'] = plan
            if isinstance(plan, ResponseContent):
                plan.refresh(token=request.auth)
                return plan

            if not 'enable' in params:
                enable = self.match_enable(plan, 10129)
                if isinstance(enable, ResponseContent):
                    enable.refresh(token=request.auth)
                    return enable

        if 'eid' in params and 'exist-enroll' in self.process_list:
            print('---------------exist-enroll-------------------')
            enroll = self.exist_enroll(params)
            self.detail['enroll'] = enroll
            if isinstance(enroll, ResponseContent):
                enroll.refresh(token=request.auth)
                return enroll

            if not 'enable' in params:
                enable = self.match_enable(enroll, 10130)
                if isinstance(enable, ResponseContent):
                    enable.refresh(token=request.auth)
                    return enable

        if 'lid' in params and 'exist-lesson' in self.process_list:
            print('---------------exist-lesson-------------------')
            lesson = self.exist_lesson(params)
            self.detail['lesson'] = lesson
            if isinstance(lesson, ResponseContent):
                lesson.refresh(token=request.auth)
                return lesson

            if not 'enable' in params:
                enable = self.match_enable(lesson, 10131)
                if isinstance(enable, ResponseContent):
                    enable.refresh(token=request.auth)
                    return enable

        if 'curid' in params and 'exist-curriculum' in self.process_list:
            print('---------------exist-curriculum-------------------')
            curriculum = self.exist_curriculum(params)
            self.detail['curriculum'] = curriculum
            if isinstance(curriculum, ResponseContent):
                curriculum.refresh(token=request.auth)
                return curriculum

            if not 'enable' in params:
                enable = self.match_enable(curriculum, 10132)
                if isinstance(enable, ResponseContent):
                    enable.refresh(token=request.auth)
                    return enable

        if 'hid' in params and 'exist-homework' in self.process_list:
            print('---------------exist-homework-------------------')
            homework = self.exist_homework(params)
            self.detail['homework'] = homework
            if isinstance(homework, ResponseContent):
                homework.refresh(token=request.auth)
                return homework

            if not 'enable' in params:
                enable = self.match_enable(homework, 10133)
                if isinstance(enable, ResponseContent):
                    enable.refresh(token=request.auth)
                    return enable

        if 'qid' in params and 'exist-question' in self.process_list:
            print('---------------exist-question-------------------')
            question = self.exist_question(params)
            self.detail['question'] = question
            if isinstance(question, ResponseContent):
                question.refresh(token=request.auth)
                return question

            if not 'enable' in params:
                enable = self.match_enable(question, 10134)
                if isinstance(enable, ResponseContent):
                    enable.refresh(token=request.auth)
                    return enable

        if 'leid' in params and 'exist-example' in self.process_list:
            print('---------------exist-example-------------------')
            example = self.exist_example(params)
            self.detail['example'] = example
            if isinstance(example, ResponseContent):
                example.refresh(token=request.auth)
                return example

            if not 'enable' in params:
                enable = self.match_enable(example, 10135)
                if isinstance(enable, ResponseContent):
                    enable.refresh(token=request.auth)
                    return enable

        if 'comment' in params and 'exist-comment' in self.process_list:
            print('---------------comment-------------------')
            comment = self.exist_comment(params)
            self.detail['comment'] = comment
            if isinstance(comment, ResponseContent):
                comment.refresh(token=request.auth)
                return comment

        # if 'mrcid' in params and 'exist-MaoRecord' in self.process_list:
        #     print('---------------exist-MaoRecord-------------------')
        #     record = self.exist_mao_record(params)
        #     self.detail['record'] = record
        #     if isinstance(record, ResponseContent):
        #         return record

        if hasattr(self, 'extra'):
            print('-----------------extra-----------------')
            match = getattr(self, 'extra')
            extra = match(request, self.detail)
            self.detail['extra'] = extra
            if isinstance(extra, ResponseContent):
                extra.refresh(token=request.auth)
                return extra

        if 'refresh-login' in self.process_list:
            print('---------------refresh-login-------------------')
            refresh_login = self.refresh_login(request, profile)
            if isinstance(refresh_login, ResponseContent):
                refresh_login.refresh(token=request.auth)
                return refresh_login

        return self.set_value(user, profile)

    def set_value(self, user, profile):
        self.detail['user'] = user
        self.detail['profile'] = profile

        content = self.detail

        self.detail = {}

        return content

