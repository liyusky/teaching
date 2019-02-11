<template>
  <!-- s  -->
  <section class="panel" id="panel" v-show="panel">
    <component :is="current"></component>
  </section>
  <!-- s  -->
</template>

<script>
// 班级
import ClassAddClassPanelComponent from '../../components/manager/class/panel/class/class.vue'
import ClassUpdateClassPanelComponent from '../../components/manager/class/panel/update-class/update-class.vue'
// 方案
import PlanAddPlanPanelComponent from '../../components/manager/class/panel/plan/plan.vue'
import PlanUpdatePlanPanelComponent from '../../components/manager/class/panel/update-plan/update-plan.vue'
// 报名
import EnrollAddEnrollPanelComponent from '../../components/manager/class/panel/enroll/enroll.vue'
import EnrollUpdateEnrollPanelComponent from '../../components/manager/class/panel/update-enroll/update-enroll.vue'
// 课程
import CourseAddCoursePanelComponent from '../../components/manager/course/panel/course/course.vue'
import CourseUpdateCoursePanelComponent from '../../components/manager/course/panel/update-course/update-course.vue'
// 课时
import LessonAddLessonPanelComponent from '../../components/manager/course/panel/lesson/lesson.vue'
import LessonUpdateLessonPanelComponent from '../../components/manager/course/panel/update-lesson/update-lesson.vue'
// 课程表
import CurriculumAddCurriculumPanelComponent from '../../components/manager/curriculum/panel/add-curriculum/add-curriculum.vue'
import CurriculumUpdateCurriculumPanelComponent from '../../components/manager/curriculum/panel/update-curriculum/update-curriculum.vue'
// 学生
import StudentAddStudentPanelComponent from '../../components/manager/student/panel/student/student.vue'
import StudentUpdateStudentPanelComponent from '../../components/manager/student/panel/update-student/update-student.vue'
// 教师
import TeacherAddTeacherPanelComponent from '../../components/manager/teacher/panel/teacher/teacher.vue'
import TeacherUpdateTeacherPanelComponent from '../../components/manager/teacher/panel/update-teacher/update-teacher.vue'
// 作业
import HomeworkAddHomeworkPanelComponent from '../../components/manager/homework/panel/homework/homework.vue'
import HomeworkUpdateHomeworkPanelComponent from '../../components/manager/homework/panel/update-homework/update-homework.vue'
// 问题
import QuestionAddQuestionPanelComponent from '../../components/manager/homework/panel/question/question.vue'
import QuestionUpdateQuestionPanelComponent from '../../components/manager/homework/panel/update-question/update-question.vue'
// 学校
// import SchoolAddSchoolPanelComponent from '../../components/manager/school/panel/add-school/add-school.vue'
// import SchoolUpdateSchoolPanelComponent from '../../components/manager/school/panel/update-school/update-school.vue'
// 案例
import ExampleAddExamplePanelComponent from '../../components/content/example/panel/add-example/add-example.vue'
import ExampleUpdateExamplePanelComponent from '../../components/content/example/panel/update-example/update-example.vue'
// 用户
import UserUpdateUserPanelComponent from '../../components/panel/user/update-user/update-user.vue'
// include dependence
export default {
  name: 'Panel',
  data () {
    return {
      panel: false,
      current: null,
      gold: {
        // 班级
        'class-add-class': ClassAddClassPanelComponent,
        'class-update-class': ClassUpdateClassPanelComponent,
        // 方案
        'plan-add-plan': PlanAddPlanPanelComponent,
        'plan-update-plan': PlanUpdatePlanPanelComponent,
        // 报名
        'enroll-add-enroll': EnrollAddEnrollPanelComponent,
        'enroll-update-enroll': EnrollUpdateEnrollPanelComponent,
        // 课程
        'course-add-course': CourseAddCoursePanelComponent,
        'course-update-course': CourseUpdateCoursePanelComponent,
        // 课时
        'lesson-add-lesson': LessonAddLessonPanelComponent,
        'lesson-update-lesson': LessonUpdateLessonPanelComponent,
        // 课程表
        'curriculum-add-curriculum': CurriculumAddCurriculumPanelComponent,
        'curriculum-update-curriculum': CurriculumUpdateCurriculumPanelComponent,
        // 学生
        'student-add-student': StudentAddStudentPanelComponent,
        'student-update-student': StudentUpdateStudentPanelComponent,
        // 教师
        'teacher-add-teacher': TeacherAddTeacherPanelComponent,
        'teacher-update-teacher': TeacherUpdateTeacherPanelComponent,
        // 作业
        'homework-add-homework': HomeworkAddHomeworkPanelComponent,
        'homework-update-homework': HomeworkUpdateHomeworkPanelComponent,
        // 问题
        'question-add-question': QuestionAddQuestionPanelComponent,
        'question-update-question': QuestionUpdateQuestionPanelComponent,
        // 学校
        // 'school-add-school': SchoolAddSchoolPanelComponent,
        // 'school-update-school': SchoolUpdateSchoolPanelComponent,
        // 案例
        'example-add-example': ExampleAddExamplePanelComponent,
        'example-update-example': ExampleUpdateExamplePanelComponent,
        // 用户
        'user-update-user': UserUpdateUserPanelComponent
      }
      // start datas
      // end datas
    }
  },
  watch: {
    '$store.state.panel' (panel) {
      if (panel === false) {
        this.panel = false
        this.current = null
      } else {
        this.panel = true
        this.current = this.gold[panel]
      }
    }
  },
  components: {
    // include chunk
    // 班级
    ClassAddClassPanelComponent,
    ClassUpdateClassPanelComponent,
    // 报名
    EnrollAddEnrollPanelComponent,
    EnrollUpdateEnrollPanelComponent,
    // 方案
    PlanAddPlanPanelComponent,
    PlanUpdatePlanPanelComponent,
    // 课程
    CourseAddCoursePanelComponent,
    CourseUpdateCoursePanelComponent,
    // 课时
    LessonAddLessonPanelComponent,
    LessonUpdateLessonPanelComponent,
    // 课程表
    CurriculumAddCurriculumPanelComponent,
    CurriculumUpdateCurriculumPanelComponent,
    // 学生
    StudentAddStudentPanelComponent,
    StudentUpdateStudentPanelComponent,
    // 教师
    TeacherAddTeacherPanelComponent,
    TeacherUpdateTeacherPanelComponent,
    // 作业
    HomeworkAddHomeworkPanelComponent,
    HomeworkUpdateHomeworkPanelComponent,
    // 问题
    QuestionAddQuestionPanelComponent,
    QuestionUpdateQuestionPanelComponent,
    // 学校
    // SchoolAddSchoolPanelComponent,
    // SchoolUpdateSchoolPanelComponent,
    // 案例
    ExampleAddExamplePanelComponent,
    ExampleUpdateExamplePanelComponent,
    // 用户
    UserUpdateUserPanelComponent
  }
}
</script>

<style lang="sass" scoped>
@import "./panel.scss";
</style>
