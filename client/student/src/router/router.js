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
          path: '/student/course',
          name: 'student-course',
          component: CourseComponent
        },
        {
          path: '/student/lesson',
          name: 'student-lesson',
          component: LessonComponent
        },
        {
          path: '/student/example',
          name: 'student-example',
          component: ExampleComponent
        },
        {
          path: '/student/example-stage',
          name: 'student-example-stage',
          component: StageComponent
        },
        {
          path: '/student/example-code',
          name: 'student-example-code',
          component: CodeComponent
        },
        {
          path: '/student/example-record',
          name: 'student-example-record',
          component: RecordComponent
        },
        {
          path: '/student/homework',
          name: 'student-homework',
          component: HomeworkComponent
        },
        {
          path: '/student/homework-stage',
          name: 'student-homework-stage',
          component: StageComponent
        },
        {
          path: '/student/homework-code',
          name: 'student-homework-code',
          component: CodeComponent
        },
        {
          path: '/student/homework-record',
          name: 'student-homework-record',
          component: RecordComponent
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
