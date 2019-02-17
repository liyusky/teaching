from .models import GameStage, Chapter, UserLangStage, UserSetting, UserLangChapter, UserStagesStatistic
# from django.core.urlresolvers import reverse
from django.urls import reverse

def getMySetting(user):
    usersettings = UserSetting.objects.filter(user=user)
    if usersettings.exists():
        return usersettings[0]
    return None

def next_stage(stage_idx):
    stages = GameStage.objects.filter(idx=stage_idx)
    if not stages.exists():
        return None
    stage = stages[0]
    chapters = stage.chapter_set.all()
    if chapters.count() == 0:
        stages = GameStage.objects.filter(idx=1)
        return stages[0]

    chapter = chapters[0]
    c_stages = chapter.stages.all().order_by('-idx')
    if c_stages[0].idx == stage.idx: #本章节最后一关
        c = Chapter.objects.filter(id=chapter.id+1)
        if c.exists():
            cp = c[0]
            return cp.stages.all().order_by('idx')[0]
        else:
            return None     #没有后续章节了
    else:
        last_stage = None
        for s in c_stages: #逆序
            if s.idx == stage.idx:
                return last_stage
            last_stage = s
    return None


def getUserLastStageInChapter(user, chapter_id):
    setting = getMySetting(user)
    chapters = Chapter.objects.filter(id=chapter_id)
    if not chapters.exists():
        return False
    chapter = chapters[0]
    c_stages = chapter.stages.all().order_by('idx')
    for stage in c_stages:  # 顺序
        statis = UserStagesStatistic.objects.filter(user=user, stage=stage, lang=setting.lang)
        if not statis.exists() or statis[0].high_score < 100:
            return stage

def unlockNewChapter(user, chapter_id):
    # setting=getMySetting(user)
    # userstage, created = UserLangStage.objects.get_or_create(user=user, lang=setting.lang)
    # userchapter, created=UserLangChapter.objects.get_or_create(userlangstage=userstage,
    #                                       chapter_id=chapter_id,
    #                                       )
    # userchapter.unlock = 1
    # userchapter.save()
    return True


def lockNewChapter(user, chapter_id):
    setting=getMySetting(user)
    userstage, created = UserLangStage.objects.get_or_create(user=user, lang=setting.lang)
    userchapter, created=UserLangChapter.objects.get_or_create(userlangstage=userstage,
                                          chapter_id=chapter_id,
                                          )
    userchapter.unlock = 0
    userchapter.save()


def isChapterUnlocked(user, chapter_id):
    # setting = getMySetting(user)
    # userstage, created = UserLangStage.objects.get_or_create(user=user, lang=setting.lang)
    # userchapter, created = UserLangChapter.objects.get_or_create(userlangstage=userstage,
    #                                                     chapter_id=chapter_id,
    #                                                     )
    # if userchapter.unlock:
    #     return True
    # return False
    return False


def isChapterFinished(user, chapter_id):
    # setting = getMySetting(user)
    # chapters = Chapter.objects.filter(id=chapter_id)
    # if not chapters.exists():
    #     return False
    # chapter = chapters[0]
    # c_stages = chapter.stages.filter(enable=True).order_by('-idx')
    # if not c_stages.exists():
    #     return False
    # last_stage = c_stages[0]
    # statistics = UserStagesStatistic.objects.fiter(user=user, stage=last_stage, lang=setting.lang)
    # if not statistics.exists():
    #     return False
    # statistic = statistics[0]
    # if statistic.high_score >= 100:
    #     return True
    # return False
    return True


def accessChapter(user, chapter_id):
    #login_init(user)
    # jump2ChapterLastStage(user, chapter_id)
    # return reverse('kudingmao:stage', args=())
    return 'https://www.bilibili.com'


def jump2ChapterLastStage(user, chapter_id):
    usersetting = getMySetting(user)
    userstages = UserLangStage.objects.filter(user=user, lang=usersetting.lang)
    if not userstages.exists():
        return False
    userstage = userstages[0]
    chapters = Chapter.objects.filter(id=chapter_id)
    if not chapters.exists():
        return False
    chapter = chapters[0]
    stage = getUserLastStageInChapter(user, chapter_id)
    stages = GameStage.objects.filter(idx=stage.idx)
    if not stages.exists():
        return False
    stage = stages[0]
    userstage.new_chapter = chapter
    userstage.new_stage = stage
    userstage.save()
    return True


def first_stage():
    chapters = Chapter.objects.filter(id=1)
    chapter = chapters[0]
    c_stages = chapter.stages.all().order_by('idx')
    return c_stages[0]

def login_init(user):
    # usersettings = UserSetting.objects.filter(user=user)
    # if not usersettings.exists():
    #     usersetting = UserSetting(user=user)
    #     usersetting.lang_id = 1
    #     usersetting.save()
    # userstage, created = UserLangStage.objects.get_or_create(user=user, lang=usersettings[0].lang,
    #                                                          defaults={
    #                                                              'new_stage': first_stage()
    #                                                          })
    return True