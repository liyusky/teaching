<template>
  <!-- s  -->
  <section class="teacher">
    <div class="teacher-nav">
      <BtnComponent :setting="btn" @BTN_CLICK_EVENT="addTeacher" class="nav-btn">
        <i></i>
        <span>新增教师</span>
      </BtnComponent>
      <!-- <SearchBarComponent :placeholder="placeholder" @SEARCH_EVENT="serach" @REFRESH_EVENT="refresh"></SearchBarComponent> -->
    </div>
    <TableComponent ref="table"></TableComponent>
    <!-- <SeparatorComponent></SeparatorComponent> -->
  </section>
  <!-- s  -->
</template>

<script>
import TableComponent from './table/table.vue'
// include dependence
import Display from '../../../../dependencies/modules/Display.class.js'
import BtnComponent from '../../../../dependencies/components/btn/btn.vue'
import SearchBarComponent from '../../../../dependencies/components/search-bar/search-bar.vue'
import SeparatorComponent from '../../../../dependencies/components/separator/separator.vue'
export default {
  name: 'TeacherComponent',
  data () {
    return {
      placeholder: '请输入姓名',
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
  methods: {
    addTeacher () {
      Display.panel = 'teacher-add-teacher'
    },
    serach (keywords) {
      this.$refs.table.getTeacherList(keywords)
    },
    refresh () {
      this.$refs.table.getTeacherList()
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./teacher.scss";
</style>
