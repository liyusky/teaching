from django.conf.urls import url, include
from .view import authentication, teachers, students, commons, manager, root
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'teaching'
url_all = []

url_auth = [
    url(r'^auth/register$', authentication.Register.as_view()),
    url(r'^auth/forget-password$', authentication.ForgetPassword.as_view()),
    url(r'^auth/login-by-password$', authentication.LoginByPassword.as_view()),
    url(r'^auth/login-by-sms$', authentication.LoginBySMSCaptcha.as_view()),
    url(r'^auth/logout$', authentication.Logout.as_view())
]

url_common = [
    url(r'^common/send-sms$', commons.SMSCaptchaView.as_view()),
    url(r'^common/image-code$', commons.CaptchaView.as_view()),
    url(r'^common/score-code$', commons.SourceCode.as_view()),
    url(r'^common/comment-single$', commons.CommentSingle.as_view()),
    # url(r'^common/school-list$', commons.SchoolList.as_view()),
    url(r'^common/update-account$', commons.UpdateAccount.as_view()),
    url(r'^common/game-url$', commons.GameUrl.as_view()),
    url(r'^common/game-stage-list$', commons.GameStageList.as_view()),
    url(r'^common/game-stage-score$', commons.GameStageScore.as_view()),
    url(r'^common/game-stage-record$', commons.GameStageRecord.as_view()),
    url(r'^common/game-is-finish$', commons.GameStageIsFinished.as_view()),
    url(r'^common/game-is-unlock$', commons.GameStageIsUnlock.as_view()),
]

url_root = [
    url(r'^root/user-bind-profile$', root.UserBindProfile.as_view()),
]

url_manager = [
    # 班级
    url(r'^manager/class-list$', manager.ClassList.as_view()),
    url(r'^manager/add-class$', manager.AddClass.as_view()),
    url(r'^manager/update-class$', manager.UpdateClass.as_view()),
    # 方案
    url(r'^manager/plan-list$', manager.PlanList.as_view()),
    url(r'^manager/add-plan$', manager.AddPlan.as_view()),
    url(r'^manager/update-plan$', manager.UpdatePlan.as_view()),
    # 报名
    url(r'^manager/enroll-list$', manager.EnrollList.as_view()),
    url(r'^manager/add-enroll$', manager.AddEnroll.as_view()),
    url(r'^manager/update-enroll$', manager.UpdateEnroll.as_view()),
    # 课程
    url(r'^manager/course-list$', manager.CourseList.as_view()),
    url(r'^manager/add-course$', manager.AddCourse.as_view()),
    url(r'^manager/update-course$', manager.UpdateCourse.as_view()),
    # 学校
    # url(r'^manager/add-school$', manager.AddSchool.as_view()),
    # url(r'^manager/update-school$', manager.UpdateSchool.as_view()),
    # 课时
    url(r'^manager/lesson-list$', manager.LessonList.as_view()),
    url(r'^manager/add-lesson$', manager.AddLesson.as_view()),
    url(r'^manager/update-lesson$', manager.UpdateLesson.as_view()),
    # 游戏
    url(r'^manager/game-chapter-list$', manager.GameChapterList.as_view()),
    url(r'^manager/game-stage-list$', manager.GameStageList.as_view()),
    # 课程表
    url(r'^manager/curriculum-list$', manager.CurriculumList.as_view()),
    url(r'^manager/add-curriculum$', manager.AddCurriculum.as_view()),
    url(r'^manager/update-curriculum$', manager.UpdateCurriculum.as_view()),
    # 教师
    url(r'^manager/teacher-list$', manager.TeacherList.as_view()),
    url(r'^manager/add-teacher$', manager.AddTeacher.as_view()),
    url(r'^manager/update-teacher$', manager.UpdateTeacher.as_view()),
    # 学生
    url(r'^manager/student-list$', manager.StudentList.as_view()),
    url(r'^manager/add-student$', manager.AddStudent.as_view()),
    url(r'^manager/update-student$', manager.UpdateStudent.as_view()),
    # 作业
    url(r'^manager/homework-list$', manager.HomeworkList.as_view()),
    url(r'^manager/add-homework$', manager.AddHomework.as_view()),
    url(r'^manager/update-homework$', manager.UpdateHomework.as_view()),
    # 问题
    url(r'^manager/question-list$', manager.QuestionList.as_view()),
    url(r'^manager/add-question$', manager.AddQuestion.as_view()),
    url(r'^manager/update-question$', manager.UpdateQuestion.as_view()),
    # 案例
    url(r'^manager/example-list$', manager.ExampleList.as_view()),
    url(r'^manager/add-example$', manager.AddExample.as_view()),
    url(r'^manager/update-example$', manager.UpdateExample.as_view()),
    # 用户
    # 作业成绩
    url(r'^manager/score-list$', manager.ScoreList.as_view()),
    # 课时内容题目成绩
    url(r'^manager/example-score-list$', manager.ExampleScoreList.as_view()),
    # 评语
    url(r'^manager/add-comment$', manager.AddComment.as_view()),
    url(r'^manager/update-comment$', manager.UpdateComment.as_view()),
    url(r'^manager/open-chapter$', manager.GameStageOpenChapter.as_view()),
    url(r'^manager/game-is-unlock$', manager.GameStageIsUnlock.as_view()),
    # url(r'^auth/login-by-password$', authentication.LoginByPasswordView.as_view()),
    # url(r'^auth/login-by-sms$', authentication.LoginBySMSCaptchaView.as_view()),
    # url(r'^auth/forget-password$', authentication.ForgetPasswordView.as_view()),
    # url(r'^teacher/course-list$', teachers.CourseListView.as_view()),
    # url(r'^teacher/course-detail$', teachers.CourseDetailView.as_view()),
    # url(r'^teacher/homework-report$', teachers.HomeworkReport.as_view()),
    # url(r'^teacher/update-comment$', teachers.CommentView.as_view()),
    # url(r'^student/course-list$', students.CourseListView.as_view()),
    # url(r'^student/course-detail$', students.CourseDetailView.as_view()),
    # url(r'^common/source-code', commons.SourceCode.as_view()),
    # url(r'^common/homework-detail', commons.HomeworkDetailView.as_view()),
]

url_student = [
    url(r'^student/course-list$', students.CourseList.as_view()),
    url(r'^student/lesson-list$', students.LessonList.as_view()),
    url(r'^student/question-score-list$', students.HomeworkDetailScoreList.as_view()),
    url(r'^student/example-score-list$', students.LessonDetailScoreList.as_view()),
]

url_teachers = [
    # 班级
    url(r'^teacher/class-list$', teachers.ClassList.as_view()),
    # 方案
    url(r'^teacher/plan-list$', teachers.PlanList.as_view()),
    # 报名
    url(r'^teacher/enroll-list$', teachers.EnrollList.as_view()),
    # 课程
    url(r'^teacher/course-list$', teachers.CourseList.as_view()),
    # 课时
    url(r'^teacher/lesson-list$', teachers.LessonList.as_view()),
    # 游戏
    url(r'^teacher/game-chapter-list$', teachers.GameChapterList.as_view()),
    # 课程表
    url(r'^teacher/curriculum-list$', teachers.CurriculumList.as_view()),
    url(r'^teacher/add-curriculum$', teachers.AddCurriculum.as_view()),
    url(r'^teacher/update-curriculum$', teachers.UpdateCurriculum.as_view()),
    # 作业
    url(r'^teacher/homework-list$', teachers.HomeworkList.as_view()),
    url(r'^teacher/add-homework$', teachers.AddHomework.as_view()),
    url(r'^teacher/update-homework$', teachers.UpdateHomework.as_view()),
    # 问题
    url(r'^teacher/question-list$', teachers.QuestionList.as_view()),
    url(r'^teacher/add-question$', teachers.AddQuestion.as_view()),
    url(r'^teacher/update-question$', teachers.UpdateQuestion.as_view()),
    # 案例
    url(r'^teacher/example-list$', teachers.ExampleList.as_view()),
    # 作业成绩
    url(r'^teacher/score-list$', teachers.ScoreList.as_view()),
    # 课时内容题目成绩
    url(r'^teacher/example-score-list$', teachers.ExampleScoreList.as_view()),
    # 游戏章节控制
    url(r'^teacher/open-chapter$', teachers.GameStageOpenChapter.as_view()),
    url(r'^teacher/game-is-unlock$', teachers.GameStageIsUnlock.as_view()),
    # 评论
    url(r'^teacher/add-comment$', teachers.AddComment.as_view()),
    url(r'^teacher/update-comment$', teachers.UpdateComment.as_view()),
]

url_all.extend(url_auth)
url_all.extend(url_common)
url_all.extend(url_manager)
url_all.extend(url_student)
url_all.extend(url_root)
url_all.extend(url_teachers)


urlpatterns = url_all
