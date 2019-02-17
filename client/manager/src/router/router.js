import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)
const LoginComponent = () => import(/* webpackChunkName: 'login' */ '../components/login/login.vue')
const ManagerComponent = () => import(/* webpackChunkName: 'manager' */ '../components/manager/manager.vue')
const ClassComponent = () => import(/* webpackChunkName: 'manager-class' */ '../components/manager/class/class.vue')
const CourseComponent = () => import(/* webpackChunkName: 'manager-course' */ '../components/manager/course/course.vue')
const CurriculumComponent = () => import(/* webpackChunkName: 'manager-curriculum' */ '../components/manager/curriculum/curriculum.vue')
const HomeworkComponent = () => import(/* webpackChunkName: 'manager-homework' */ '../components/manager/homework/homework.vue')
const LessonScoreComponent = () => import(/* webpackChunkName: 'manager-lesson-score' */ '../components/manager/lesson-score/lesson-score.vue')
// const SchoolComponent = () => import(/* webpackChunkName: 'manager-school' */ '../components/manager/school/school.vue')
const ScoreComponent = () => import(/* webpackChunkName: 'manager-score' */ '../components/manager/score/score.vue')
const StudentComponent = () => import(/* webpackChunkName: 'manager-student' */ '../components/manager/student/student.vue')
const TeacherComponent = () => import(/* webpackChunkName: 'manager-teacher' */ '../components/manager/teacher/teacher.vue')
const UserComponent = () => import(/* webpackChunkName: 'manager-user' */ '../components/manager/user/user.vue')

export default new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginComponent
    },
    {
      path: '/manager',
      name: 'manager',
      component: ManagerComponent,
      children: [
        {
          path: '/manager/class',
          name: 'manager-class',
          component: ClassComponent
        },
        {
          path: '/manager/course',
          name: 'manager-course',
          component: CourseComponent
        },
        {
          path: '/manager/curriculum',
          name: 'manager-curriculum',
          component: CurriculumComponent
        },
        {
          path: '/manager/homework',
          name: 'manager-homework',
          component: HomeworkComponent
        },
        {
          path: '/manager/lesson-score',
          name: 'manager-lesson-score',
          component: LessonScoreComponent
        },
        // {
        //   path: '/manager/school',
        //   name: 'manager-school',
        //   component: SchoolComponent
        // },
        {
          path: '/manager/score',
          name: 'manager-score',
          component: ScoreComponent
        },
        {
          path: '/manager/student',
          name: 'manager-student',
          component: StudentComponent
        },
        {
          path: '/manager/teacher',
          name: 'manager-teacher',
          component: TeacherComponent
        },
        {
          path: '/manager/user',
          name: 'manager-user',
          component: UserComponent
        }
      ],
      redirect: '/class'
    },
    {
      path: '*',
      redirect: 'login'
    }
  ]
})
