<template>
  <!-- s  -->
  <section class="curriculum">
    <div class="curriculum-nav">
      <div class="nav-btns">
        <button class="btns-item" @click="addCurriculum">排布课时</button>
      </div>
      <div class="nav-select">
        <div class="select-item fl" @click="selectClass">{{organization}}</div>
        <div class="select-item fl" @click="selectCourse">{{course}}</div>
      </div>
    </div>
    <CurriculumTableComponent :oid="oid" :cid="cid" :course="course" :organization="organization"></CurriculumTableComponent>
  </section>
  <!-- s  -->
</template>

<script>
import CurriculumTableComponent from './table/table.vue'
// include dependence
import Communication from '../../../../dependencies/modules/Communication.class.js'
import Dictionary from '../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../dependencies/modules/Display.class.js'
import Account from '../../../../dependencies/modules/Account.class.js'

export default {
  name: 'CurriculumComponent',
  data () {
    return {
      organization: '选择班级',
      course: '选择课程',
      oid: 0,
      cid: 0
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
    CurriculumTableComponent
  },
  mounted () {
    Account.logout()
  },
  methods: {
    selectCourse () {
      Display.modal = 'course-select'
    },
    selectClass () {
      Display.modal = 'class-select'
    },
    addCurriculum () {
      if (this.course === '选择课程') {
        alert('未选择课程')
        return
      }
      if (this.organization === '选择班级') {
        alert('未选择班级')
        return
      }
      Communication.panel = {
        cid: this.cid,
        oid: this.oid,
        course: this.course,
        organization: this.organization
      }
      Display.panel = 'curriculum-add-curriculum'
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
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./curriculum.scss";
</style>
