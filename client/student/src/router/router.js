import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)
const LoginComponent = () => import(/* webpackChunkName: 'login' */ '../components/login/login.vue')
const StudentComponent = () => import(/* webpackChunkName: 'student' */ '../components/student/student.vue')
const CodeComponent = () => import(/* webpackChunkName: 'student-code' */ '../components/student/code/code.vue')
const CourseComponent = () => import(/* webpackChunkName: 'student-course' */ '../components/student/course/course.vue')
const ExampleComponent = () => import(/* webpackChunkName: 'student-example' */ '../components/student/example/example.vue')
const HomeworkComponent = () => import(/* webpackChunkName: 'student-homework' */ '../components/student/homework/homework.vue')
const LessonComponent = () => import(/* webpackChunkName: 'student-lesson' */ '../components/student/lesson/lesson.vue')
const RecordComponent = () => import(/* webpackChunkName: 'student-record' */ '../components/student/record/record.vue')
const StageComponent = () => import(/* webpackChunkName: 'student-stage' */ '../components/student/stage/stage.vue')

export default new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginComponent
    },
    {
      path: '/student',
      name: 'student',
      component: StudentComponent,
      children: [
        {
          path: '/student/code',
          name: 'student-code',
          component: CodeComponent
        },
        {
          path: '/student/course',
          name: 'student-course',
          component: CourseComponent
        },
        {
          path: '/student/example',
          name: 'student-example',
          component: ExampleComponent
        },
        {
          path: '/student/homework',
          name: 'student-homework',
          component: HomeworkComponent
        },
        {
          path: '/student/lesson',
          name: 'student-lesson',
          component: LessonComponent
        },
        {
          path: '/student/record',
          name: 'student-record',
          component: RecordComponent
        },
        {
          path: '/student/stage',
          name: 'student-stage',
          component: StageComponent
        }
      ],
      redirect: '/student/course'
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
