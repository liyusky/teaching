from django.db import models
from django.contrib.auth.models import User


GAME_TYPE_CHOICES = (
    (0, '酷町猫'),
    (1, '酷町打字'),
)


BOOLEAN_CHOICES = (
    (0, False),
    (1, True),
)

SEX_CHOICES = (
    (0, '女'),
    (1, '男'),
)

GRADE_CHOICES = (
    (0, '未知'),
    (1, '小一'),
    (2, '小二'),
    (3, '小三'),
    (4, '小四'),
    (5, '小五'),
    (6, '小六'),
    (7, '初一'),
    (8, '初二'),
    (9, '初三'),
    (10, '高一'),
    (11, '高二'),
    (12, '高三'),
)

LEVEL_CHOICES = (
    (0, '未定'),
    (1, '综合'),
    (2, '小学'),
    (3, '初中'),
    (4, '高中'),
)



class SMS(models.Model):
    SCENE_CHOICES = (
        (0, '登陆'),
        (1, '注册'),
        (2, '忘记密码'),
    )
    USED_CHOICES = (
        (0, '未使用'),
        (1, '已使用'),
    )
    secret = models.CharField(max_length=6)
    phone = models.CharField(max_length=13, unique=True)
    send_time = models.DateTimeField(auto_now_add=False, null=True)
    end_time = models.DateTimeField(auto_now_add=False, null=True)
    scene = models.IntegerField(choices=SCENE_CHOICES, null=True)
    used = models.IntegerField(choices=USED_CHOICES, null=True, default=0)



class SMSRecord(models.Model):
    SCENE_CHOICES = (
        (0, '登陆'),
        (1, '注册'),
        (2, '忘记密码'),
    )
    sms = models.ForeignKey(SMS, on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=20, default=None)
    cp_name = models.CharField(max_length=20, default=None)
    smsid = models.CharField(max_length=64, default=None)
    secret_sign = models.CharField(max_length=64, default=None)
    compute_sign = models.CharField(max_length=64, default=None)
    send_time = models.DateTimeField(auto_now_add=False, null=True)
    end_time = models.DateTimeField(auto_now_add=False, null=True)
    scene = models.IntegerField(choices=SCENE_CHOICES)



# class School(models.Model):
#     name = models.CharField(max_length=50)
#     district = models.CharField(max_length=50, null=True, default=None)
#     level = models.IntegerField(default=None, null=True, choices=LEVEL_CHOICES)
#     enable = models.BooleanField(default=1, choices=BOOLEAN_CHOICES)

#     def __str__(self):
#         return self.name


# class CourseLocation(models.Model):
#     name = models.CharField(max_length=50, default="")
#     address = models.CharField(max_length=200, default="")
#     enable = models.BooleanField(default=1, choices=BOOLEAN_CHOICES)


class UserTeachingProfile(models.Model):
    ROLE_CHOICES = (
        (0, '学生'),
        (1, '教学老师'),
        (2, '教务老师'),
        (3, '教务主任'),
        (4, '教学主任'),
        (99, '管理员'),
        (100, 'root'),
    )
    user = models.OneToOneField(User, null=False, on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=11, blank=True)
    name = models.CharField(max_length=50, default='')
    sex = models.IntegerField(default=0, choices=SEX_CHOICES)
    role = models.IntegerField(default=0, choices=ROLE_CHOICES)  # 用户类型
    age = models.IntegerField(default=None, null=True)
    # school = models.ForeignKey(School, default=None, null=True)
    grade = models.IntegerField(default=0, choices=GRADE_CHOICES)
    creator = models.IntegerField(default=-1)
    description = models.TextField(default='', null=True)
    login_time = models.DateTimeField(auto_now_add=False, null=True)
    enable = models.BooleanField(default=1, choices=BOOLEAN_CHOICES)
    ip = models.CharField(max_length=15, default=None)


class Course(models.Model):
    LANGUAGE_CHOICES = (
        (0, '未定'),
        (1, '综合'),
        (2, 'PASCAL'),
        (3, 'C'),
        (4, 'C++'),
    )
    GRADE_CHOICES = (
        (0, '未定'),
        (1, '综合'),
        (2, '小学'),
        (3, '初中'),
        (4, '高中'),
    )
    name = models.CharField(default="", max_length=300)
    language = models.IntegerField(choices=LANGUAGE_CHOICES, default=0)
    grade = models.IntegerField(choices=GRADE_CHOICES, default=0)
    description = models.TextField(default="")
    creator = models.ForeignKey(User, default=1, on_delete=models.SET_NULL, null=True)
    create_time = models.DateTimeField(auto_now_add=False, null=True)
    enable = models.BooleanField(default=1, choices=BOOLEAN_CHOICES)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING,)
    name = models.CharField(default="", max_length=200)
    description = models.TextField(default="")
    creator = models.ForeignKey(User, default=1, on_delete=models.DO_NOTHING, limit_choices_to={'role__gt': 0, 'enable': 1})
    create_time = models.DateTimeField(auto_now_add=False, null=True)
    enable = models.BooleanField(default=1, choices=BOOLEAN_CHOICES)

    def __str__(self):
        return self.name

class LessonDetail(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.DO_NOTHING, limit_choices_to={'enable': 1})
    gametype = models.IntegerField(default=0, choices=GAME_TYPE_CHOICES)
    gcid = models.IntegerField(default=0) #章节id
    gsid = models.IntegerField(default=0) #关卡id
    idx = models.IntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=False, null=True)
    enable = models.BooleanField(default=1, choices=BOOLEAN_CHOICES)



class Cls(models.Model):
    name = models.CharField(max_length=200,default="")
    description = models.TextField(default="")
    courses = models.ManyToManyField(Course, through='ClsCourse', blank=True)
    students = models.ManyToManyField(User, through='ClsStudent', through_fields=('cls', 'student'), blank=True)
    teacher = models.ForeignKey(User, related_name='ClsTeacher', default=1, on_delete=models.DO_NOTHING)
    #location = models.ForeignKey(CourseLocation, default=1, on_delete=models.DO_NOTHING) #上课地点
    start_time = models.DateTimeField(auto_now_add=False, null=True)
    end_time = models.DateTimeField(auto_now_add=False, null=True)
    creator = models.ForeignKey(User, related_name='ClsCreator', default=1, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=False, null=True)
    enable = models.BooleanField(default=1, choices=BOOLEAN_CHOICES)

    def __str__(self):
        return self.name


class ClsStudent(models.Model):
    STATUS_CHOICES = (
        (0, '未决定'),
        (1, '学习中'),
        (2, '结业'),
        (3, '肄业'),
    )
    cls = models.ForeignKey(Cls, on_delete=models.CASCADE, limit_choices_to={'enable': 1})
    #course = models.ForeignKey(Course, on_delete=models.CASCADE, limit_choices_to={'enable': 1})
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 0, 'enable': 1})
    creator = models.ForeignKey(User, related_name='ClsStudentCreator', default=1, on_delete=models.DO_NOTHING, limit_choices_to={'role__gt': 0, 'enable': 1})
    create_time = models.DateTimeField(auto_now_add=False, null=True)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    enable = models.BooleanField(default=1, choices=BOOLEAN_CHOICES)


class ClsCourse(models.Model):
    cls = models.ForeignKey(Cls, on_delete=models.CASCADE, limit_choices_to={'enable': 1})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, limit_choices_to={'enable': 1})
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__gt': 0, 'enable': 1})
    #school = models.ForeignKey(School, default=1, on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField(auto_now_add=False, null=True)
    end_time = models.DateTimeField(auto_now_add=False, null=True)
    creator = models.ForeignKey(User, default=1, related_name='ClsCourseCreator', on_delete=models.DO_NOTHING, limit_choices_to={'role__gt': 0, 'enable': 1})
    create_time = models.DateTimeField(auto_now_add=False, null=True)
    enable = models.BooleanField(default=1, choices=BOOLEAN_CHOICES)


#排课表
class Curriculum(models.Model):
    cls = models.ForeignKey(Cls, on_delete=models.CASCADE, limit_choices_to={'enable': 1})
    #course = models.ForeignKey(Course, on_delete=models.CASCADE, limit_choices_to={'enable': 1})
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, limit_choices_to={'enable': 1})
    #school = models.ForeignKey(School, default=1, on_delete=models.DO_NOTHING)
    classroom = models.CharField(max_length=200, default="", null=True)
    start_time = models.DateTimeField(auto_now_add=False, null=True)
    end_time = models.DateTimeField(auto_now_add=False, null=True)
    task = models.BooleanField(default=0, choices=BOOLEAN_CHOICES)
    creator = models.ForeignKey(User, default=1, related_name='CurriculumCreator', on_delete=models.DO_NOTHING, limit_choices_to={'role__gt': 0, 'enable': 1})
    create_time = models.DateTimeField(auto_now_add=False, null=True)
    enable = models.BooleanField(default=1, choices=BOOLEAN_CHOICES)



class Homework(models.Model):
    name = models.CharField(max_length=200)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, limit_choices_to={'enable': 1})
    start_time = models.DateTimeField(auto_now_add=False, null=True)
    end_time = models.DateTimeField(auto_now_add=False, null=True)
    description = models.TextField(default="")
    creator = models.ForeignKey(User, default=1, on_delete=models.DO_NOTHING, limit_choices_to={'role__gt': 0, 'enable': 1})
    create_time = models.DateTimeField(auto_now_add=False, null=True)
    enable = models.BooleanField(default=1, choices=BOOLEAN_CHOICES)



class HomeworkDetail(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.DO_NOTHING, limit_choices_to={'enable': 1})
    gametype = models.IntegerField(choices=GAME_TYPE_CHOICES, default=0)
    gsid = models.IntegerField(default=0) #具体关卡id
    gcid = models.IntegerField(default=0) #章节id
    idx = models.IntegerField(default=0)
    creator = models.ForeignKey(User, default=1, on_delete=models.DO_NOTHING, limit_choices_to={'role': 0, 'enable': 1})
    create_time = models.DateTimeField(auto_now_add=False, null=True)
    enable = models.BooleanField(default=1, choices=BOOLEAN_CHOICES)



class Comment(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='CommentStudent', on_delete=models.DO_NOTHING, limit_choices_to={'role': 0, 'enable': 1})
    #teacher = models.ForeignKey(User, related_name='CommentTeacher', on_delete=models.DO_NOTHING, limit_choices_to={'role__gt': 0, 'enable': 1})
    content = models.TextField(default="")
