<template>
  <!-- s  -->
  <section class="detail">
    <p class="detail-header">
      <span class="header-name">{{name}}</span>
      <span class="header-tip">班级：{{organization}}，课程：{{course}}，课时：{{lesson}}</span>
    </p>
    <component :is="current"></component>
  </section>
  <!-- s  -->
</template>

<script>
import CodeDetailComponent from './code/code.vue'
import SummaryDetailComponent from './summary/summary.vue'
// include dependence
import Communication from '../../../../../dependencies/modules/Communication.class.js'

export default {
  name: 'DetailComponent',
  data () {
    return {
      name: `${Communication.detail.name}（${Communication.detail.phone}）`,
      current: null,
      organization: Communication.detail.organization,
      course: Communication.detail.course,
      lesson: Communication.detail.lesson
    }
  },
  created () {
    let components = {
      'code': CodeDetailComponent,
      'summary': SummaryDetailComponent
    }
    this.current = components[Communication.detail.component]
  },
  components: {
    // include chunk
    CodeDetailComponent,
    SummaryDetailComponent
  }
}
</script>

<style lang="sass" scoped>
@import "./detail.scss";
</style>
