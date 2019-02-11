from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from uuid import uuid4

def map_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = filename.split('.')[-1]
    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ext:" + ext);
    return 'kdmgame/data/map/map_{0}.{1}'.format(str(instance.idx) + "_" + str(uuid4().hex), ext)

class Lang(models.Model):
    TL0 = 100
    TL1 = 1000  # ms
    TL2 = 2000
    TL3 = 3000
    TL4 = 4000
    TL5 = 5000
    TL6 = 6000
    TL7 = 7000
    TL8 = 8000
    TL9 = 9000
    TL10 = 10000
    TIME_LIMIT_CHOICES = (
        (TL0, '100ms'),
        (TL1, '1s'),
        (TL2, '2s'),
        (TL3, '3s'),
        (TL4, '4s'),
        (TL5, '5s'),
        (TL6, '6s'),
        (TL7, '7s'),
        (TL8, '8s'),
        (TL9, '9s'),
        (TL10, '10s'),
    )
    MEMORY_LIMIT_CHOICES = (
        (131072, '128MB'),
        (65536, '64MB'),
    )

    name = models.CharField(max_length=20)
    verbose_name = models.CharField(max_length=100)
    time_limit = models.IntegerField(choices=TIME_LIMIT_CHOICES, default=TL0)
    memory_limit = models.IntegerField(choices=MEMORY_LIMIT_CHOICES, default=131072)


    def __str__(self):
        return self.verbose_name


class GameStage(models.Model): #游戏关卡

    name = models.CharField(max_length=100, default="")
    map = models.FileField(upload_to=map_directory_path, blank=True, null=True)#场景地图表
    #hint = models.TextField(default="")
    hint = MarkdownxField(default="")
    idx = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_map = self.map
            self.map = None
            super(GameStage, self).save(*args, **kwargs)
            self.map = saved_map

        super(GameStage, self).save(*args, **kwargs)

    # Create a property that returns the markdown instead
    @property
    def hint_formatted_markdown(self):
        return markdownify(self.hint)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    TYPE_NORMAL = 0
    TYPE_EXAM = 1
    TYPE_CHOICES = (
        (TYPE_NORMAL, '普通'),
        (TYPE_EXAM, '考试'),
    )
    title = models.CharField(max_length=200)
    enable = models.BooleanField(default=False)
    stages = models.ManyToManyField(GameStage)
    btn_enable = models.CharField(max_length=500, default="")
    type = models.IntegerField(default=0, choices=TYPE_CHOICES)


    def __str__(self):
        return self.title


class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lang = models.ForeignKey(Lang, on_delete=models.CASCADE)


class UserLangStage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lang = models.ForeignKey(Lang, default=1, on_delete=models.CASCADE)
    last_stage = models.ForeignKey(GameStage, default=1, on_delete=models.CASCADE)
    new_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, default=1) #最后章节
    new_stage = models.ForeignKey(GameStage, on_delete=models.CASCADE, default=1, related_name='userlangstage_new_stage') #最后关卡
    chapters = models.ManyToManyField(Chapter, through='UserLangChapter', related_name='userlang_chapters')

    class Meta:
        unique_together = [
            ['user', 'lang'],
        ]

#用户章节解锁情况
class UserLangChapter(models.Model):
    userlangstage = models.ForeignKey(UserLangStage, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    unlock = models.IntegerField(default=0) #0表示未解锁

    class Meta:
        unique_together = [
            ['userlangstage', 'chapter'],
        ]

class UserStagesStatistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stage = models.ForeignKey(GameStage, on_delete=models.CASCADE)
    lang = models.ForeignKey(Lang, default=1, on_delete=models.CASCADE)
    high_score = models.IntegerField(default=0)

    class Meta:
        unique_together = [
            ['user', 'stage', 'lang'],
        ]


class StageLang(models.Model):
    STL_NOR = 0
    STL_FILL = 1  # ms
    STAGE_LANG_TYPE = (
        (STL_NOR, '普通'),
        (STL_FILL, '补全'),
    )
    stage = models.ForeignKey(GameStage, on_delete=models.CASCADE)
    lang = models.ForeignKey(Lang, on_delete=models.CASCADE)
    min_lines = models.IntegerField(default=0)
    fish_count = models.IntegerField(default=0)
    hint = MarkdownxField(default="")
    default_code = models.TextField(default="", blank=True)
    type = models.IntegerField(default=STL_NOR, choices=STAGE_LANG_TYPE)

    @property
    def hint_formatted_markdown(self):
        return markdownify(self.hint)

    def __str__(self):
        return self.stage.name + " " + self.lang.verbose_name

    class Meta:
        unique_together = [
            ['stage', 'lang'],
        ]


class Role(models.Model):
    ME = 1
    ENEMY = 2
    FRIEND = 3
    ITEM = 4

    TYPE_CHOICES = (
        (ME, '主角'),
        (ENEMY, '敌人'),
        (FRIEND, '友军'),
        (ITEM, '道具'),
    )

    name = models.CharField(max_length=100, unique=True)
    type = models.IntegerField(default=ME, choices=TYPE_CHOICES) #角色类型
    range = models.IntegerField(default=0) #攻击范围
    hp = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class StageRole(models.Model):
    stage = models.ForeignKey(GameStage, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    ord_x = models.IntegerField(default=0) #角色位置x坐标
    ord_y = models.IntegerField(default=0) #角色位置y坐标
    dir = models.IntegerField(default=0) #角色朝向
    status = models.IntegerField(default=0) #角色状态， 0表示随机状态，状态取值根据各个role来确定

    class Meta:
        index_together = [
            ['stage', 'role'],
        ]


class StageRoleStatus(models.Model):
    stagerole = models.ForeignKey(StageRole, on_delete=models.CASCADE)
    key = models.CharField(default="", max_length=100)
    value = models.CharField(default="", max_length=100)

    class Meta:
        unique_together = ("stagerole", "key")


class UserStageStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stage = models.ForeignKey(GameStage, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "stage")


class JudgeRecord(models.Model):
    # CATEGORY_NORMAL = 0
    # CATEGORY_EXAM_NOIP = 1
    # CATEGORY_EXAM_ACM = 2
    # CATEGORY_CHOICES = (
    #     (CATEGORY_NORMAL, 'normal'),
    #     (CATEGORY_EXAM_NOIP, 'exam_noip'),
    #     (CATEGORY_EXAM_ACM, 'exam_acm'),
    # )
    Unknown=0
    Accepted=1
    Presentation_Error=2
    Time_Limit_Exceeded=3
    Memory_Limit_Exceeded=4
    Wrong_Answer=5
    Runtime_Error=6
    Output_Limit_Exceeded=7
    Compile_Error=8
    System_Error=9
    Check_Failed=10

    TYPE_NORMAL = 0
    TYPE_TEST = 1

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stage = models.ForeignKey(GameStage, on_delete=models.SET_NULL, null=True)
    code = models.TextField(default="")
    origin_code = models.TextField(default="")
    #code_type = models.CharField(max_length=100, default="")
    code_type = models.ForeignKey(Lang, on_delete=models.CASCADE)
    result = models.CharField(max_length=1000) #成功，超时，RE，编译错误等
    result_code = models.IntegerField(default=0)
    output = models.TextField()#输出结果
    score = models.IntegerField(default=0) #得分，根据fish_count和代码长度确定
    judge_time = models.DateTimeField(auto_now_add=True, null=True)
    submit_ip = models.GenericIPAddressField(null=True, blank=True)
    success = models.BooleanField(default=False)
    fish_count = models.IntegerField(default=0) #一共接到多少鱼
    type = models.IntegerField(default=TYPE_NORMAL)


    class Meta:
        index_together = [
            ['user', 'stage'],
        ]
