<template>
  <!-- s  -->
  <section class="update-plan">
    <div class="plan-header">
      <p class="header-title">更新课程</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="plan-operation">
      <ul class="operation-setting-list">
        <!-- <li class="list-item">
          <label class="item-label" for="plan-setting-update-name">班级：</label>
          <input class="item-input" id="plan-setting-update-manager" type="text" readonly="readonly" v-model="organization" placeholder="请点击选择课程" @click="selectClass">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="plan-setting-update-name">课程：</label>
          <input class="item-input" id="plan-setting-update-manager" type="text" readonly="readonly" v-model="course" placeholder="请点击选择课程" @click="selectCourse">
        </li>
        <li class="list-item">
          <label class="item-label" for="plan-setting-update-teacher">老师：</label>
          <input class="item-input" id="plan-setting-update-teacher" type="text" readonly="readonly" v-model="teacher" placeholder="请点击选择教师" @click="selectTeacher">
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="plan-setting-update-school">学校：</label>
          <input class="item-input" id="plan-setting-add-teacher" type="text" readonly="readonly" v-model="college" placeholder="请点击选择学校" @click="selectSchool">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="plan-setting-update-date">开课时间：</label>
          <flat-pickr
            class="item-pickr"
            v-model="date"
            :config="config"
            id="plan-setting-update-date"></flat-pickr>
        </li>
      </ul>
      <section class="operation-btns">
        <button class="btns-confirm" :disabled="confirmDisabled" @click="confirm">确认</button>
        <button class="btns-cancel" @click="cancel">取消</button>
      </section>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
import 'flatpickr/dist/flatpickr.css'
import 'flatpickr/dist/themes/dark.css'
import 'flatpickr/dist/l10n/zh.js'
import flatPickr from 'vue-flatpickr-component'
// include dependence
import Check from '../../../../../../dependencies/modules/Check.class.js'
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Dictionary from '../../../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'
import Time from '../../../../../../dependencies/modules/Time.class.js'

export default {
  name: 'PlanUpdatePlanPanelComponent',
  data () {
    return {
      oid: '',
      cid: '',
      tid: '',
      pid: '',
      organization: '',
      course: '',
      teacher: '',
      // school: 1,
      // college: '',
      date: '',
      teacherid: 0,
      config: {
        mode: 'range',
        wrap: true,
        altInput: true,
        altFormat: 'Y/m/d',
        dateFormat: 'Z'
      },
      confirmDisabled: false
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
    flatPickr
  },
  created () {
    let panel = {...Communication.panel}
    this.data = {...Communication.panel}
    this.oid = panel.oid
    this.cid = panel.cid
    this.tid = panel.tid
    this.pid = panel.pid
    // this.school = panel.school
    // this.college = `${panel.college.name}${panel.college.district || ''}${Dictionary.rank[panel.college.level]}`
    this.organization = panel.organization.name
    this.data.date = `${Time.format('YYYY/MM/DD', panel.launch)} to ${Time.format('YYYY/MM/DD', panel.deadline)}`
    this.date = `${Time.format('YYYY/MM/DD', panel.launch)} to ${Time.format('YYYY/MM/DD', panel.deadline)}`
    this.teacher = `${panel.teacherDetail.name}（${panel.teacherDetail.phone}）`
    this.course = `${panel.courseDetail.name}（${Dictionary.language[panel.courseDetail.language]}，${Dictionary.rank[panel.courseDetail.grade]}）`
  },
  methods: {
    // selectSchool () {
    //   Display.modal = 'school-select'
    // },
    selectTeacher () {
      Display.modal = 'teacher-select'
    },
    selectCourse () {
      Display.modal = 'course-select'
    },
    selectClass () {
      Display.modal = 'class-select'
    },
    confirm () {
      if (!Check.dateRange(this.date)) return
      let data = {pid: this.pid}

      if (this.data.oid !== this.oid) {
        data.oid = this.oid
        data.cls = this.oid
      }
      if (this.data.tid !== this.tid) {
        data.teacher = this.teacherid
        data.tid = this.tid
      }
      if (this.data.cid !== this.cid) {
        data.course = this.cid
        data.cid = this.cid
      }
      // if (this.school && this.data.school !== this.school) data.school = this.school
      if (this.data.date !== this.date) {
        data.launch = this.date.split(' to ')[0]
        data.deadline = this.date.split(' to ')[1]
      }

      Http.send({
        url: 'UpdatePlan',
        data: data
      }).before(() => {
        this.confirmDisabled = true
      }).success(data => {
        Display.api = 'PlanList'
      }).fail(data => {
      }).default(() => {
        this.confirmDisabled = false
        Display.panel = false
      })
    },
    cancel () {
      Display.panel = false
      Communication.modal = false
      this.clear()
    },
    clear () {
      this.cid = ''
      this.tid = ''
      this.course = ''
      this.teacher = ''
      // this.school = 1
      this.date = ''
    }
  },
  watch: {
    '$store.state.modal' (modal, previous) {
      if (previous === 'teacher-select' && modal === false && Communication.modal) {
        this.teacher = `${Communication.modal.detail.realname}（${Communication.modal.phone}）`
        this.tid = {...Communication.modal}.upid
        this.teacherid = {...Communication.modal}.user
      } else if (previous === 'course-select' && modal === false && Communication.modal) {
        this.course = `${Communication.modal.name}（${Dictionary.language[Communication.modal.language]}，${Dictionary.rank[Communication.modal.grade]}）`
        this.cid = {...Communication.modal}.cid
      } else if (previous === 'class-select' && modal === false && Communication.modal) {
        this.organization = `${Communication.modal.name}（${Communication.modal.manager.name} ${Communication.modal.manager.phone}）`
        this.oid = {...Communication.modal}.oid
      }
      // else if (previous === 'school-select' && modal === false && Communication.modal) {
      //   this.college = `${Communication.modal.name}${Communication.modal.district}${Dictionary.rank[Communication.modal.level]}`
      //   this.school = {...Communication.modal}.school
      // }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./update-plan.scss";
</style>
