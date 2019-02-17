<template>
  <!-- s  -->
  <section class="add-curriculum">
    <div class="curriculum-header">
      <p class="header-title">
        <span class="title-name">设置课时时间</span>
      </p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="curriculum-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="curriculum-setting-add-class">班级：</label>
          <input class="item-input" id="curriculum-setting-add-class" type="text" readonly="readonly" v-model="organization">
        </li>
        <li class="list-item">
          <label class="item-label" for="curriculum-setting-add-course">课程：</label>
          <input class="item-input" id="curriculum-setting-add-course" type="text" readonly="readonly" v-model="course">
        </li>
        <li class="list-item">
          <label class="item-label" for="curriculum-setting-add-lesson">课时：</label>
          <input class="item-input" id="curriculum-setting-add-lesson" type="text" readonly="readonly" v-model="lesson" placeholder="请点击选择课程" @click="selectLesson">
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="curriculum-setting-add-school">学校：</label>
          <input class="item-input" id="plan-setting-add-teacher" type="text" readonly="readonly" v-model="college" placeholder="请点击选择学校" @click="selectSchool">
        </li> -->
        <!-- <li class="list-item">
          <label class="item-label" for="curriculum-setting-add-classroom">教室：</label>
          <input class="item-input" id="curriculum-setting-add-classroom" type="text" v-model="classroom" placeholder="请输入教室">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="curriculum-setting-add-date">课时时间：</label>
          <flat-pickr
            class="item-pickr"
            v-model="date"
            :config="config"
            id="curriculum-setting-add-date"></flat-pickr>
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
// import Dictionary from '../../../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'CurriculumAddCurriculumPanelComponent',
  data () {
    return {
      oid: '',
      cid: '',
      lid: '',
      lesson: '',
      // school: 0,
      // college: '',
      classroom: '',
      date: '',
      organization: '未选择班级',
      course: '未选择课程',
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
    this.oid = Communication.panel.oid
    this.cid = Communication.panel.cid
    this.organization = Communication.panel.organization
    this.course = Communication.panel.course
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
      if (!Check.dateRange(this.date)) return
      // if (!Check.appellation(this.classroom)) return
      Http.send({
        url: 'AddCurriculum',
        data: {
          oid: this.oid,
          cls: this.oid,
          lid: this.lid,
          lesson: this.lid,
          cid: this.cid,
          // school: this.school,
          // classroom: this.classroom,
          launch: this.date.split(' to ')[0],
          deadline: this.date.split(' to ')[1]
        }
      }).success(data => {
        Display.api = 'CurriculumList'
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
      this.oid = ''
      this.cid = ''
      this.lid = ''
      this.lesson = ''
      // this.school = 1
      // this.classroom = ''
      this.date = ''
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
@import "./add-curriculum.scss";
</style>
