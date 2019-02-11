<template>
  <!-- s  -->
  <section class="school">
    <div class="school-nav">
      <BtnComponent :setting="btn" @BTN_CLICK_EVENT="addSchool" class="nav-btn">
        <i></i>
        <span>新增学校地址</span>
      </BtnComponent>
      <BtnComponent :setting="btn" @BTN_CLICK_EVENT="refresh" class="nav-btn">
        <i></i>
        <span>刷新</span>
      </BtnComponent>
    </div>
    <SchoolTableComponent ref="table"></SchoolTableComponent>
    <!-- <SeparatorComponent></SeparatorComponent> -->
  </section>
  <!-- s  -->
</template>

<script>
import SchoolTableComponent from './table/table.vue'
// include dependence
import Display from '../../../../dependencies/modules/Display.class.js'
import BtnComponent from '../../../../dependencies/components/btn/btn.vue'
import SeparatorComponent from '../../../../dependencies/components/separator/separator.vue'
export default {
  name: 'SchoolComponent',
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
    SeparatorComponent,
    BtnComponent,
    // include chunk
    SchoolTableComponent
  },
  methods: {
    addSchool () {
      Display.panel = 'school-add-school'
    },
    refresh () {
      this.$refs.table.getSchoolList()
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./school.scss";
</style>
