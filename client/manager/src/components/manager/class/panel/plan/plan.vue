<template>
  <!-- s  -->
  <section class="plan">
    <div class="plan-header">
      <p class="header-title">添加课程</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="plan-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="plan-setting-add-name">课程：</label>
          <input class="item-input" id="plan-setting-add-manager" type="text" readonly="readonly" v-model="course" placeholder="请点击选择课程" @click="selectCourse">
        </li>
        <li class="list-item">
          <label class="item-label" for="plan-setting-add-teacher">老师：</label>
          <input class="item-input" id="plan-setting-add-teacher" type="text" readonly="readonly" v-model="teacher" placeholder="请点击选择教师" @click="selectTeacher">
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="plan-setting-add-school">学校：</label>
          <input class="item-input" id="plan-setting-add-teacher" type="text" readonly="readonly" v-model="college" placeholder="请点击选择学校" @click="selectSchool">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="plan-setting-add-date">开课时间：</label>
          <flat-pickr
            class="item-pickr"
            v-model="date"
            :config="config"
            id="plan-setting-add-date"></flat-pickr>
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
// import Account from '../../../../../../dependencies/modules/Account.class.js'
import Check from '../../../../../../dependencies/modules/Check.class.js'
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Dictionary from '../../../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'PlanAddPlanPanelComponent',
  data () {
    return {
      oid: '',
      cid: '',
      tid: '',
      course: '',
      teacher: '',
      // school: '',
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
    this.oid = Communication.panel.oid
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
    confirm () {
      if (!Check.dateRange(this.date)) return
      Http.send({
        url: 'AddPlan',
        data: {
          oid: this.oid,
          cid: this.cid,
          cls: this.oid,
          teacher: this.teacherid,
          course: this.cid,
          // school: this.school,
          launch: this.date.split(' to ')[0],
          deadline: this.date.split(' to ')[1]
        }
      }).success(data => {
        Display.api = 'PlanList'
      }).fail(data => {
      }).default(() => {
        this.confirmDisabled = false
        this.cancel()
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
      // this.school = ''
      this.date = ''
    }
  },
  watch: {
    '$store.state.modal' (modal, previous) {
      console.log(modal, previous, Communication.modal)
      if (previous === 'teacher-select' && modal === false && Communication.modal) {
        this.teacher = `${Communication.modal.name}（${Communication.modal.phone}）`
        this.tid = {...Communication.modal}.upid
        this.teacherid = {...Communication.modal}.user
      } else if (previous === 'course-select' && modal === false && Communication.modal) {
        this.course = `${Communication.modal.name}（${Dictionary.language[Communication.modal.language]}，${Dictionary.rank[Communication.modal.grade]} ）`
        this.cid = {...Communication.modal}.cid
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
@import "./plan.scss";
</style>
