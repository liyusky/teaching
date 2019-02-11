<template>
  <!-- s  -->
  <section class="modal" id="modal" v-show="modal">
    <component :is="current"></component>
  </section>
  <!-- s  -->
</template>

<script>
import TeacherSelectModalComponent from '../../components/modal/teacher-select/teacher-select.vue'
import CourseSelectModalComponent from '../../components/modal/course-select/course-select.vue'
import ClassSelectModalComponent from '../../components/modal/class-select/class-select.vue'
import StudentSelectModalComponent from '../../components/modal/student-select/student-select.vue'
import LessonSelectModalComponent from '../../components/modal/lesson-select/lesson-select.vue'
import GameStageSelectModalComponent from '../../components/modal/game-stage-select/game-stage-select.vue'
import GameChapterSelectModalComponent from '../../components/modal/game-chapter-select/game-chapter-select.vue'
// import SchoolSelectModalComponent from '../../components/modal/school-select/school-select.vue'
// include dependence
export default {
  name: 'Modal',
  data () {
    return {
      modal: false,
      current: null,
      gold: {
        'teacher-select': TeacherSelectModalComponent,
        'course-select': CourseSelectModalComponent,
        'class-select': ClassSelectModalComponent,
        'student-select': StudentSelectModalComponent,
        'lesson-select': LessonSelectModalComponent,
        'game-stage-select': GameStageSelectModalComponent,
        'game-chapter-select': GameChapterSelectModalComponent
        // 'school-select': SchoolSelectModalComponent
      }
      // start datas
      // end datas
    }
  },
  watch: {
    '$store.state.modal' (modal) {
      if (modal === false) {
        this.modal = false
        this.current = null
      } else {
        this.modal = true
        this.current = this.gold[modal]
      }
    }
  },
  components: {
    // include chunk
    TeacherSelectModalComponent,
    CourseSelectModalComponent,
    ClassSelectModalComponent,
    StudentSelectModalComponent,
    LessonSelectModalComponent,
    GameStageSelectModalComponent,
    GameChapterSelectModalComponent
    // SchoolSelectModalComponent
  }
}
</script>

<style lang="sass" scoped>
@import "./modal.scss";
</style>
