<template>
  <!-- s  -->
  <section class="student">
    <div class="student-nav">
      <button class="nav-btn" @click="addStudent">新增学员</button>
      <div class="student-operation">
        <button class="nav-btn" :disabled="bindProfileDisabled" @click="bindProfile">拉取所有用户</button>
        <SearchBarComponent @SEARCH_EVENT="search" @REFRESH_EVENT="refresh"></SearchBarComponent>
      </div>
    </div>
    <TableComponent ref="table" @User_Bind_Profile_OPEN_EVENT="openBindProfileDisabled"></TableComponent>
    <!-- <SeparatorComponent></SeparatorComponent> -->
  </section>
  <!-- s  -->
</template>

<script>
import TableComponent from './table/table.vue'
// include dependence
import Account from '../../../../dependencies/modules/Account.class.js'
import Display from '../../../../dependencies/modules/Display.class.js'
import SearchBarComponent from '../../../../dependencies/components/search-bar/search-bar.vue'
export default {
  name: 'StudentComponent',
  data () {
    return {
      bindProfileDisabled: false
      // start datas
      // end datas
    }
  },
  components: {
    SearchBarComponent,
    TableComponent
  },
  mounted () {
    Account.logout()
  },
  methods: {
    addStudent () {
      Display.panel = 'student-add-student'
    },
    bindProfile () {
      if (Account.role !== 100) {
        alert('您不具备root权限')
        return
      }
      this.bindProfileDisabled = true
      this.$refs.table.bindProfile()
    },
    refresh (keywords) {
      this.$refs.table.getStudentList(keywords)
    },
    search (keywords) {
      this.$refs.table.getStudentList(keywords)
    },
    openBindProfileDisabled () {
      this.bindProfileDisabled = false
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./student.scss";
</style>
