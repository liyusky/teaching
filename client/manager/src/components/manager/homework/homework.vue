<template>
  <!-- s 作业管理 -->
  <section class="homework">
    <div class="homework-nav">
      <div class="nav-select">
        <div class="select-item fl" @click="selectClass">{{organization}}</div>
        <div class="select-item fl" @click="selectCourse">{{course}}</div>
        <div class="select-item fl" @click="selectLesson">{{lesson}}</div>
      </div>
    </div>
    <TableComponent :oid="oid" :cid="cid" :lid="lid"></TableComponent>
    <!-- <SeparatorComponent></SeparatorComponent> -->
  </section>
  <!-- s 作业管理 -->
</template>

<script>
import TableComponent from './table/table.vue'
// include dependence
import Communication from '../../../../dependencies/modules/Communication.class.js'
import Dictionary from '../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../dependencies/modules/Display.class.js'
import Account from '../../../../dependencies/modules/Account.class.js'
import SearchBarComponent from '../../../../dependencies/components/search-bar/search-bar.vue'
import SeparatorComponent from '../../../../dependencies/components/separator/separator.vue'
export default {
  name: 'HomeworkComponent',
  data () {
    return {
      chapters: [],
      oid: 0,
      cid: 0,
      lid: 0,
      gcid: 0,
      organization: '选择班级',
      course: '选择课程',
      lesson: '选择课时'
      // start datas
      // end datas
    }
  },
  components: {
    SearchBarComponent,
    SeparatorComponent,
    // include chunk
    TableComponent
  },
  mounted () {
    Account.logout()
  },
  methods: {
    selectLesson () {
      if (this.cid <= 0) {
        alert('请选择课程')
        return
      }
      Communication.modal = this.cid
      Display.modal = 'lesson-select'
    },
    selectCourse () {
      Display.modal = 'course-select'
    },
    selectClass () {
      Display.modal = 'class-select'
    }
  },
  watch: {
    '$store.state.modal' (modal, previous) {
      if (previous === 'course-select' && modal === false && Communication.modal) {
        this.course = `${Communication.modal.name}（${Dictionary.language[Communication.modal.language]}，${Dictionary.rank[Communication.modal.grade]}）`
        this.cid = {...Communication.modal}.cid
        Communication.modal = false
      } else if (previous === 'class-select' && modal === false && Communication.modal) {
        this.organization = `${Communication.modal.name}（${Communication.modal.manager.name} ${Communication.modal.manager.phone}）`
        this.oid = {...Communication.modal}.oid
        Communication.modal = false
      } else if (previous === 'lesson-select' && modal === false && Communication.modal) {
        this.lesson = Communication.modal.name
        this.lid = {...Communication.modal}.lid
        Communication.modal = false
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./homework.scss";
</style>
