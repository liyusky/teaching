<template>
  <!-- s 班级管理 -->
  <section class="class">
    <div class="class-nav">
      <BtnComponent :setting="btn" @BTN_CLICK_EVENT="addClass" class="nav-btn">
        <i></i>
        <span>新添班级</span>
      </BtnComponent>
      <BtnComponent :setting="btn" @BTN_CLICK_EVENT="refresh" class="nav-btn">
        <i></i>
        <span>刷新</span>
      </BtnComponent>
      <!-- <SearchBarComponent></SearchBarComponent> -->
    </div>
    <ClassTableComponent ref="table"></ClassTableComponent>
    <!-- <SeparatorComponent></SeparatorComponent> -->
  </section>
  <!-- s 班级管理 -->
</template>

<script>
import ClassTableComponent from './table/class/class.vue'
// include dependence
import Display from '../../../../dependencies/modules/Display.class.js'
import Account from '../../../../dependencies/modules/Account.class.js'
import BtnComponent from '../../../../dependencies/components/btn/btn.vue'
import SearchBarComponent from '../../../../dependencies/components/search-bar/search-bar.vue'
import SeparatorComponent from '../../../../dependencies/components/separator/separator.vue'
export default {
  name: 'ClassComponent',
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
    SearchBarComponent,
    SeparatorComponent,
    BtnComponent,
    // include chunk
    ClassTableComponent
  },
  mounted () {
    Account.logout()
  },
  methods: {
    addClass () {
      Display.panel = 'class-add-class'
    },
    refresh () {
      this.$refs.table.getClassList()
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./class.scss";
</style>
