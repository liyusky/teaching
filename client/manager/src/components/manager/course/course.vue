<template>
  <!-- s 课程管理 -->
  <section class="course">
    <div class="course-nav">
      <BtnComponent :setting="btn" @BTN_CLICK_EVENT="addCourse" class="nav-btn">
        <i></i>
        <span>新增课程</span>
      </BtnComponent>
      <BtnComponent :setting="btn" @BTN_CLICK_EVENT="refresh" class="nav-btn">
        <i></i>
        <span>刷新</span>
      </BtnComponent>
      <!-- <SearchBarComponent></SearchBarComponent> -->
    </div>
    <TableComponent ref="table"></TableComponent>
    <!-- <SeparatorComponent></SeparatorComponent> -->
  </section>
  <!-- s 课程管理 -->
</template>

<script>
import TableComponent from './table/table.vue'
// include dependence
import Display from '../../../../dependencies/modules/Display.class.js'
import Account from '../../../../dependencies/modules/Account.class.js'
import BtnComponent from '../../../../dependencies/components/btn/btn.vue'
import SearchBarComponent from '../../../../dependencies/components/search-bar/search-bar.vue'
import SeparatorComponent from '../../../../dependencies/components/separator/separator.vue'
export default {
  name: 'CourseComponent',
  data () {
    return {
      // start datas
      btn: {
        type: 'addition'
      }
      // end datas
    }
  },
  components: {
    BtnComponent,
    SearchBarComponent,
    SeparatorComponent,
    // include chunk
    TableComponent
  },
  mounted () {
    Account.logout()
  },
  methods: {
    addCourse () {
      Display.panel = 'course-add-course'
    },
    refresh () {
      this.$refs.table.getCourseList()
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./course.scss";
</style>
