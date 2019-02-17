import uuid
import time
import re

from django.contrib.auth.models import User
from rest_framework import serializers
from teaching.models import *
from django.utils import timezone
from kudingmao.models import GameStage as MaoGameStage, Chapter as MaoGameChapter, UserStagesStatistic as MaoScore, \
    JudgeRecord as MaoRecord
from teaching.sms_captcha import SMSCaptcha





# class SchoolSerializer(serializers.ModelSerializer):
#     school = serializers.IntegerField(source='id')
#     class Meta:
#         model = School
#         fields = ('school', 'name', 'district', 'level', 'enable')



class UserSerializer(serializers.ModelSerializer):
    uid = serializers.IntegerField(source='id')


    class Meta:
        model = User
        fields = ('uid', 'username', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, email='')
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        if 'first_name' in validated_data:
            instance.first_name = validated_data.get('first_name', instance.first_name)
        if 'last_name' in validated_data:
            instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance



class UserProfileSerializer(serializers.ModelSerializer):
    upid = serializers.IntegerField(source='id')
    detail = serializers.SerializerMethodField()

    class Meta:
        model = UserTeachingProfile
        fields = ('upid', 'user', 'phone', 'name', 'sex', 'role', 'age', 'grade', 'detail', 'creator', 'description', 'enable')

    def create(self, validated_data):
        validated_data['ip'] = '127.0.0.1'

        profile = UserTeachingProfile.objects.create(**validated_data)
        return profile

    def update(self, instance, validated_data):
        if 'phone' in validated_data:
            instance.phone = validated_data.get('phone', instance.phone)
        if 'name' in validated_data:
            instance.name = validated_data.get('name', instance.name)
        if 'sex' in validated_data:
            instance.sex = validated_data.get('sex', instance.sex)
        if 'age' in validated_data:
            instance.age = validated_data.get('age', instance.age)
        if 'enroll' in validated_data:
            instance.enroll = validated_data.get('enroll', instance.enroll)
        if 'role' in validated_data:
            instance.role = validated_data.get('role', instance.role)
        if 'enable' in validated_data:
            instance.enable = validated_data.get('enable', instance.enable)
        # if 'school' in validated_data:
        #     instance.school = validated_data.get('school', instance.school)
        if 'grade' in validated_data:
            instance.grade = validated_data.get('grade', instance.grade)
        if 'description' in validated_data:
            instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    def get_detail(self, row):
        user = row.user
        creator = row
        if row.creator > 0:
            creator = UserTeachingProfile.objects.get(user=row.creator)

        result = {
            'realname': user.first_name + user.last_name,
            'creator': {
                'name': creator.name,
                'phone': creator.phone
            }
        }

        # if row.school:
        #     result['college'] = {
        #         'name': row.school.name,
        #         'district': row.school.district,
        #         'level': row.school.level,
        #     }

        return result



class CourseSerializer(serializers.ModelSerializer):
    cid = serializers.IntegerField(source='id')
    creater = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('cid', 'name', 'language', 'grade', 'creator', 'creater', 'description', 'enable')

    def create(self, validated_data):
        validated_data['create_time'] = timezone.now()
        course = Course.objects.create(**validated_data)
        return course

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            instance.name = validated_data.get('name', instance.name)
        if 'language' in validated_data:
            instance.language = validated_data.get('language', instance.language)
        if 'grade' in validated_data:
            instance.grade = validated_data.get('grade', instance.grade)
        if 'enable' in validated_data:
            instance.enable = validated_data.get('enable', instance.enable)
        if 'description' in validated_data:
            instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    def get_creater(self, row):
        creator = row.creator.userteachingprofile

        return {
            'name': row.creator.first_name + row.creator.last_name,
            'phone': creator.phone
        }


class LessonSerializer(serializers.ModelSerializer):
    lid = serializers.IntegerField(source='id')
    creater = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('lid', 'name', 'course', 'creator', 'creater', 'description', 'enable')

    def create(self, validated_data):
        validated_data['create_time'] = timezone.now()
        lesson = Lesson.objects.create(**validated_data)
        return lesson

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            instance.name = validated_data.get('name', instance.name)
        if 'course' in validated_data:
            instance.course = validated_data.get('course', instance.course)
        if 'enable' in validated_data:
            instance.enable = validated_data.get('enable', instance.enable)
        if 'description' in validated_data:
            instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    def get_creater(self, row):
        creator = row.creator.userteachingprofile

        return {
            'name': row.creator.first_name + row.creator.last_name,
            'phone': creator.phone
        }


class ClassSerializer(serializers.ModelSerializer):
    oid = serializers.IntegerField(source='id')
    launch = serializers.DateTimeField(source='start_time')
    deadline = serializers.DateTimeField(source='end_time')
    creater = serializers.SerializerMethodField()
    manager = serializers.SerializerMethodField()
    # college = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()

    class Meta:
        model = Cls
        fields = ('oid', 'name', 'description', 'teacher', 'detail', 'manager', 'courses', 'students', 'launch', 'deadline', 'creator', 'creater', 'enable')

    def create(self, validated_data):
        validated_data['create_time'] = timezone.now()
        organization = Cls.objects.create(**validated_data)
        return organization

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            instance.name = validated_data.get('name', instance.name)
        if 'teacher' in validated_data:
            instance.teacher = validated_data.get('teacher', instance.teacher)
        # if 'school' in validated_data:
        #     instance.school = validated_data.get('school', instance.school)
        if 'start_time' in validated_data:
            instance.start_time = validated_data.get('start_time', instance.start_time)
        if 'end_time' in validated_data:
            instance.end_time = validated_data.get('end_time', instance.end_time)
        if 'enable' in validated_data:
            instance.enable = validated_data.get('enable', instance.enable)
        if 'description' in validated_data:
            instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    def get_creater(self, row):
        creator = row.creator.userteachingprofile

        return {
            'name': row.creator.first_name + row.creator.last_name,
            'phone': creator.phone
        }

    def get_manager(self, row):
        manager = row.teacher.userteachingprofile
        return {
            'name': row.teacher.first_name + row.teacher.last_name,
            'phone': manager.phone
        }

    # def get_college(self, row):
    #     school = row.school
    #     return {
    #         'id': school.id,
    #         'name': school.name,
    #         'district': school.district,
    #         'level': school.level
    #     }

    def get_detail(self, row):
        plan = row.clscourse_set.all()
        result = {
            'name': row.name,
            'launch': row.start_time,
            'deadline': row.end_time,
            'course': []
        }

        for item in plan:
            result['course'].append({
                'course': {
                    'id': item.course.id,
                    'name': item.course.name,
                    'language': item.course.language,
                    'grade': item.course.grade,
                },
                'teacher': {
                    'tid': item.teacher.id,
                    'tpid': item.teacher.userteachingprofile.id,
                    'name': item.teacher.first_name + item.teacher.last_name,
                    'phone': item.teacher.userteachingprofile.phone
                },
                'launch': item.start_time,
                'deadline': item.end_time
            })

        return result


# ClsCourse
class PlanSerializer(serializers.ModelSerializer):
    pid = serializers.IntegerField(source='id')
    launch = serializers.DateTimeField(source='start_time')
    deadline = serializers.DateTimeField(source='end_time')
    creater = serializers.SerializerMethodField()
    # college = serializers.SerializerMethodField()
    teacherDetail = serializers.SerializerMethodField()
    courseDetail = serializers.SerializerMethodField()

    class Meta:
        model = ClsCourse
        fields = ('pid', 'cls', 'course', 'teacher', 'courseDetail', 'teacherDetail', 'launch', 'deadline', 'creator', 'creater', 'enable')

    def create(self, validated_data):
        validated_data['create_time'] = timezone.now()
        plan = ClsCourse.objects.create(**validated_data)
        return plan

    def update(self, instance, validated_data):
        if 'cls' in validated_data:
            instance.cls = validated_data.get('cls', instance.cls)
        if 'course' in validated_data:
            instance.course = validated_data.get('course', instance.course)
        if 'teacher' in validated_data:
            instance.teacher = validated_data.get('teacher', instance.teacher)
        # if 'school' in validated_data:
        #     instance.school = validated_data.get('school', instance.school)
        if 'start_time' in validated_data:
            instance.start_time = validated_data.get('start_time', instance.start_time)
        if 'end_time' in validated_data:
            instance.end_time = validated_data.get('end_time', instance.end_time)
        if 'enable' in validated_data:
            instance.enable = validated_data.get('enable', instance.enable)
        instance.save()
        return instance

    def get_courseDetail(self, row):
        course = row.course

        return {
            'name': course.name,
            'language': course.language,
            'grade': course.grade,
        }

    def get_teacherDetail(self, row):
        teacher = row.teacher.userteachingprofile

        return {
            'name': row.teacher.first_name + row.teacher.last_name,
            'phone': teacher.phone
        }

    def get_creater(self, row):
        creator = row.creator.userteachingprofile

        return {
            'name': row.creator.first_name + row.creator.last_name,
            'phone': creator.phone
        }

    # def get_college(self, row):
    #     school = row.school
    #     return {
    #         'id': school.id,
    #         'name': school.name,
    #         'district': school.district,
    #         'level': school.level
    #     }

# ClsStudent
class EnrollSerializer(serializers.ModelSerializer):
    eid = serializers.IntegerField(source='id')
    creater = serializers.SerializerMethodField()
    studentDetail = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    # plan = serializers.SerializerMethodField()

    class Meta:
        model = ClsStudent
        fields = ('eid', 'cls', 'student', 'studentDetail', 'organization', 'status', 'creator', 'creater', 'enable')

    def create(self, validated_data):
        validated_data['create_time'] = timezone.now()
        enroll = ClsStudent.objects.create(**validated_data)
        return enroll

    def update(self, instance, validated_data):
        if 'cls' in validated_data:
            instance.cls = validated_data.get('cls', instance.cls)
        if 'student' in validated_data:
            instance.student = validated_data.get('student', instance.student)
        if 'status' in validated_data:
            instance.status = validated_data.get('status', instance.status)
        if 'enable' in validated_data:
            instance.enable = validated_data.get('enable', instance.enable)
        instance.save()
        return instance

    def get_creater(self, row):
        creator = row.creator.userteachingprofile

        return {
            'name': row.creator.first_name + row.creator.last_name,
            'phone': creator.phone
        }

    def get_studentDetail(self, row):
        student = row.student.userteachingprofile

        return {
            'id': student.id,
            'name': row.student.first_name + row.student.last_name,
            'phone': student.phone
        }

    def get_organization(self, row):
        organization = row.cls
        return {
            'id': organization.id,
            'name': organization.name,
            'launch': organization.start_time,
            'deadline': organization.end_time
        }



class CurriculumSerializer(serializers.ModelSerializer):
    curid = serializers.IntegerField(source='id')
    launch = serializers.DateTimeField(source='start_time')
    deadline = serializers.DateTimeField(source='end_time')
    creater = serializers.SerializerMethodField()
    # college = serializers.SerializerMethodField()
    lessonDetail = serializers.SerializerMethodField()

    class Meta:
        model = Curriculum
        fields = ('curid', 'cls', 'lesson', 'lessonDetail', 'launch', 'deadline', 'creator', 'creater', 'task', 'enable')

    def create(self, validated_data):
        validated_data['create_time'] = timezone.now()
        enroll = Curriculum.objects.create(**validated_data)
        return enroll

    def update(self, instance, validated_data):
        if 'lesson' in validated_data:
            instance.lesson = validated_data.get('lesson', instance.lesson)
        # if 'school' in validated_data:
        #     instance.school = validated_data.get('school', instance.school)
        # if 'classroom' in validated_data:
        #     instance.classroom = validated_data.get('classroom', instance.classroom)
        if 'start_time' in validated_data:
            instance.start_time = validated_data.get('start_time', instance.start_time)
        if 'end_time' in validated_data:
            instance.end_time = validated_data.get('end_time', instance.end_time)
        if 'task' in validated_data and instance.task == 0:
            instance.task = validated_data.get('task', instance.task)
        if 'enable' in validated_data:
            instance.enable = validated_data.get('enable', instance.enable)
        instance.save()
        return instance

    def get_creater(self, row):
        creator = row.creator.userteachingprofile

        return {
            'name': row.creator.first_name + row.creator.last_name,
            'phone': creator.phone
        }

    # def get_college(self, row):
    #     school = row.school
    #     return {
    #         'id': school.id,
    #         'name': school.name,
    #         'district': school.district,
    #         'level': school.level
    #     }

    def get_lessonDetail(self, row):
        return row.lesson.name


class MaoGameChapterSerializer(serializers.ModelSerializer):
    gcid = serializers.IntegerField(source='id')

    class Meta:
        model = MaoGameChapter
        fields = ('gcid', 'title')


class MaoGameStageSerializer(serializers.ModelSerializer):
    gsid = serializers.IntegerField(source='id')
    class Meta:
        model = MaoGameStage
        fields = ('gsid', 'name')


# LessonDetail
class ExampleSerializer(serializers.ModelSerializer):
    leid = serializers.IntegerField(source='id')
    detail = serializers.SerializerMethodField()

    class Meta:
        model = LessonDetail
        fields = ('leid', 'lesson', 'idx', 'gametype', 'gsid', 'gcid', 'idx', 'detail', 'creator', 'enable')


    def create(self, validated_data):
        validated_data['create_time'] = timezone.now()
        example = LessonDetail.objects.create(**validated_data)
        return example

    def update(self, instance, validated_data):
        if 'gametype' in validated_data:
            instance.gametype = validated_data.get('gametype', instance.gametype)
        # if 'gsid' in validated_data:
        #     instance.gsid = validated_data.get('gsid', instance.gsid)
        if 'idx' in validated_data:
            instance.idx = validated_data.get('idx', instance.idx)
        if 'gcid' in validated_data:
            instance.gcid = validated_data.get('gcid', instance.gcid)
        if 'enable' in validated_data:
            instance.enable = validated_data.get('enable', instance.enable)
        instance.save()
        return instance

    def get_detail(self, row):
        creator = row.creator.userteachingprofile
        # game_stage = MaoGameStage.objects.get(pk=row.gsid)
        game_chapter = MaoGameChapter.objects.get(pk=row.gcid)

        return {
            # 'stage': game_stage.name,
            'chapter': game_chapter.title,
            'creator': {
                'name': row.creator.first_name + row.creator.last_name,
                'phone': creator.phone
            }
        }


class HighScoreSerializer(serializers.ModelSerializer):
    sid = serializers.SerializerMethodField()


    class Meta:
        model = MaoScore
        fields = ('sid', 'stage', 'lang', 'high_score',)
        depth = 1

    def get_sid(self, row):
        return row.user.id



class LessonDetailHighScoreSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()

    class Meta:
        model = LessonDetail
        fields = ('score', 'detail', 'lesson', 'gametype', 'gsid', 'gcid',)

    def get_score(self, row):
        score = []
        data = []
        if row.gametype == 0:
            score = MaoScore.objects.filter(stage=row.gsid)

        if row.gametype == 1:
            pass

        for item in score:
            data.append({
                'sid': item.user.id,
                'score': item.high_score
            })

        return data

    def get_detail(self, row):
        game_stage = MaoGameStage.objects.get(pk=row.gsid)
        game_chapter = MaoGameChapter.objects.get(pk=row.gcid)

        return {
            'stage': game_stage.name,
            'chapter': game_chapter.title,
        }





class CommentSerializer(serializers.ModelSerializer):
    comment = serializers.IntegerField(source='id')

    class Meta:
        model = Comment
        fields = ('comment', 'homework', 'student', 'content')



class HomeworkSerializer(serializers.ModelSerializer):
    hid = serializers.IntegerField(source='id')
    launch = serializers.DateTimeField(source='start_time')
    deadline = serializers.DateTimeField(source='end_time')
    curriculumDetail = serializers.SerializerMethodField()
    creater = serializers.SerializerMethodField()

    class Meta:
        model = Homework
        fields = ('hid', 'name', 'curriculum', 'curriculumDetail', 'launch', 'deadline', 'description', 'creator', 'creater', 'enable')

    def create(self, validated_data):
        validated_data['create_time'] = timezone.now()
        homework = Homework.objects.create(**validated_data)
        return homework

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            instance.name = validated_data.get('name', instance.name)
        if 'enable' in validated_data:
            instance.enable = validated_data.get('enable', instance.enable)
        if 'start_time' in validated_data:
            instance.start_time = validated_data.get('start_time', instance.start_time)
        if 'end_time' in validated_data:
            instance.end_time = validated_data.get('end_time', instance.end_time)
        if 'description' in validated_data:
            instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    def get_creater(self, row):
        creator = row.creator.userteachingprofile
        print(creator)

        return {
            'name': row.creator.first_name + row.creator.last_name,
            'phone': creator.phone
        }

    def get_curriculumDetail(self, row):
        curriculum = row.curriculum
        print(curriculum)

        return {
            'oid': curriculum.cls.id,
            'lid': curriculum.lesson.id,
            'lesson': curriculum.lesson.name,
            'organization': {
                'id': curriculum.cls.id,
                'name': curriculum.cls.name,
                'manger': {
                    'name': curriculum.cls.teacher.first_name + curriculum.cls.teacher.last_name,
                    'phone': curriculum.cls.teacher.userteachingprofile.phone
                }
            }
        }


class QuestionSerializer(serializers.ModelSerializer):
    qid = serializers.IntegerField(source='id')
    detail = serializers.SerializerMethodField()

    class Meta:
        model = HomeworkDetail
        fields = ('qid', 'homework', 'gametype', 'gsid', 'idx', 'gcid', 'detail', 'creator', 'enable')


    def create(self, validated_data):
        validated_data['create_time'] = timezone.now()
        question = HomeworkDetail.objects.create(**validated_data)
        return question

    def update(self, instance, validated_data):
        if 'gametype' in validated_data:
            instance.gametype = validated_data.get('gametype', instance.gametype)
        if 'idx' in validated_data:
            instance.idx = validated_data.get('idx', instance.idx)
        # if 'gsid' in validated_data:
        #     instance.gsid = validated_data.get('gsid', instance.gsid)
        if 'gcid' in validated_data:
            instance.gcid = validated_data.get('gcid', instance.gcid)
        if 'enable' in validated_data:
            instance.enable = validated_data.get('enable', instance.enable)
        instance.save()
        return instance

    def get_detail(self, row):
        creator = row.creator.userteachingprofile
        # game_stage = MaoGameStage.objects.get(pk=row.gsid)
        game_chapter = MaoGameChapter.objects.get(pk=row.gcid)
        return {
            # 'stage': game_stage.name,
            'chapter': game_chapter.title,
            'creator': {
                'name': row.creator.first_name + row.creator.last_name,
                'phone': creator.phone
            }
        }


class MaoStageSerializer(serializers.ModelSerializer):
    gsid = serializers.IntegerField(source='id')
    index = serializers.IntegerField(source='idx')

    class Meta:
        model = MaoGameStage
        fields = ('gsid', 'name', 'index')


class MaoScoreSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(source='high_score')
    stage = MaoStageSerializer()

    class Meta:
        model = MaoScore
        fields = ('user', 'stage', 'score')


class MaoRecordSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(source='judge_time')
    mrcid = serializers.IntegerField(source='id')


    class Meta:
        model = MaoRecord
        fields = ('mrcid', 'score', 'time', 'success')
