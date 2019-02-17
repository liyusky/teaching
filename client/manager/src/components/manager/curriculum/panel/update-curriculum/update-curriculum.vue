<template>
  <!-- s  -->
  <section class="update-curriculum">
    <div class="curriculum-header">
      <p class="header-title">
        <span class="title-name">修改课时时间</span>
      </p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="curriculum-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="curriculum-setting-update-class">班级：</label>
          <input class="item-input" id="curriculum-setting-update-class" type="text" readonly="readonly" v-model="organization">
        </li>
        <li class="list-item">
          <label class="item-label" for="curriculum-setting-update-course">课程：</label>
          <input class="item-input" id="curriculum-setting-update-course" type="text" readonly="readonly" v-model="course">
        </li>
        <li class="list-item">
          <label class="item-label" for="curriculum-setting-update-lesson">课时：</label>
          <input class="item-input" id="curriculum-setting-update-lesson" type="text" readonly="readonly" v-model="lesson" @click="selectLesson">
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="curriculum-setting-update-school">学校：</label>
          <input class="item-input" id="plan-setting-add-teacher" type="text" readonly="readonly" v-model="college" placeholder="请点击选择学校" @click="selectSchool">
        </li> -->
        <!-- <li class="list-item">
          <label class="item-label" for="curriculum-setting-update-classroom">教室：</label>
          <input class="item-input" id="curriculum-setting-update-classroom" type="text" v-model="classroom">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="curriculum-setting-update-date">课时时间：</label>
          <flat-pickr
            class="item-pickr"
            v-model="date"
            :config="config"
            id="curriculum-setting-update-date"></flat-pickr>
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
// import Dictionary from '../../../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'CurriculumUpdateCurriculumPanelComponent',
  data () {
    return {
      oid: '',
      cid: '',
      lid: '',
      curid: '',
      lesson: '',
      // school: 1,
      // college: '',
      classroom: '',
      date: '',
      organization: '',
      course: '',
      config: {
        mode: 'range',
        enableTime: true,
        wrap: true,
        altInput: true,
        altFormat: 'Y/m/d H:i',
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
    console.log(Communication.panel)
    let panel = {...Communication.panel}
    this.data = {...Communication.panel}
    this.oid = panel.oid
    this.cid = panel.cid
    this.lid = panel.lid
    this.curid = panel.curid
    this.lesson = panel.lessonDetail
    this.course = panel.course
    this.organization = panel.organization
    // this.school = panel.school
    // this.college = `${panel.college.name}${panel.college.district || ''}${Dictionary.rank[panel.college.level]}`
    // this.classroom = panel.classroom
    this.date = `${panel.launch.replace('Z', '.000Z')} to ${panel.deadline.replace('Z', '.000Z')}`
    this.data.date = `${panel.launch.replace('Z', '.000Z')} to ${panel.deadline.replace('Z', '.000Z')}`
  },
  methods: {
    // selectSchool () {
    //   Display.modal = 'school-select'
    // },
    selectLesson () {
      if (this.cid > 0) Communication.modal = this.cid
      Display.modal = 'lesson-select'
    },
    confirm () {
      let data = {
        curid: this.curid,
        curriculum: this.curid
      }
      if (this.data.lid !== this.lid) {
        data.lid = this.lid
        data.lesson = this.lid
      }
      // if (this.school && this.data.school !== this.school) data.school = this.school

      // if (this.data.classroom !== this.classroom) {
      //   if (!Check.appellation(this.classroom)) return
      //   data.classroom = this.classroom
      // }

      if (this.data.date !== this.date) {
        if (!Check.dateRange(this.date)) return
        data.launch = this.date.split(' to ')[0]
        data.deadline = this.date.split(' to ')[1]
      }

      Http.send({
        url: 'UpdateCurriculum',
        data: data
      }).before(() => {
        this.confirmDisabled = true
      }).success(data => {
        Display.api = 'CurriculumList'
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
      this.oid = ''
      this.cid = ''
      this.lid = ''
      this.curid = ''
      // this.school = ''
      this.date = ''
      this.lesson = ''
      // this.classroom = ''
    }
  },
  watch: {
    '$store.state.modal' (modal, previous) {
      if (previous === 'lesson-select' && Display.modal === false && Communication.modal) {
        this.lesson = Communication.modal.name
        this.lid = {...Communication.modal}.lid
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
@import "./update-curriculum.scss";
</style>
