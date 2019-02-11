<template>
  <!-- s 详情页 -->
  <section class="detail-page" id="detail" v-show="detail">
    <div class="page-panel">
      <component :is="current"></component>
      <aside class="panel-roll-back" @click="closeDetail">
        <div class="back-sign">
          <i>></i>
        </div>
      </aside>
    </div>
  </section>
  <!-- s 详情页 -->
</template>

<script>
import CourseDetailComponent from '../../components/manager/course/detail/detail.vue'
import ClassDetailComponent from '../../components/manager/class/detail/detail.vue'
import HomeworkDetailComponent from '../../components/manager/homework/detail/detail.vue'
import CodeDetailComponent from '../../components/manager/score/detail/detail.vue'
import LessonCodeDetailComponent from '../../components/manager/lesson-score/detail/detail.vue'
// include dependence
import Display from '../../../dependencies/modules/Display.class.js'

export default {
  name: 'DetailComponent',
  data () {
    return {
      current: null,
      detail: false,
      gold: {
        'class': ClassDetailComponent,
        'course': CourseDetailComponent,
        'homework': HomeworkDetailComponent,
        'code': CodeDetailComponent,
        'lesson-code': LessonCodeDetailComponent
      }
      // start datas
      // end datas
    }
  },
  watch: {
    '$store.state.detail' (detail) {
      if (detail) {
        this.detail = true
        this.current = this.gold[detail]
      }
    }
  },
  components: {
    // include chunk
  },
  methods: {
    closeDetail () {
      this.detail = false
      Display.detail = false
      this.current = null
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./detail.scss";
</style>
