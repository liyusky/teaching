<template>
  <!-- s  -->
  <section class="update-class">
    <div class="class-header">
      <p class="header-title">
        <span class="title-main">修改班级信息</span>
        <span class="title-tip">（班级编号 {{oid}}）</span>
      </p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="class-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="course-setting-update-name">名称：</label>
          <input class="item-input" id="course-setting-update-name" type="text" v-model="name">
        </li>
        <li class="list-item">
          <label class="item-label" for="class-setting-update-manager">班主任：</label>
          <input class="item-input" id="class-setting-update-manager" type="text" readonly="readonly" v-model="manager" placeholder="请点击选择教师" @click="selectTeacher">
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="class-setting-update-school">学校：</label>
          <input class="item-input" id="class-setting-update-school" type="text" readonly="readonly" v-model="college" placeholder="请点击选择学生所属学校" @click="selectSchool" @keyup.enter="confirm" @keyup.esc="cancel">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="class-setting-update-date">开班时间：</label>
          <flat-pickr
            class="item-pickr"
            v-model="date"
            :config="config"
            id="class-setting-update-date"></flat-pickr>
        </li>
        <li class="list-item">
          <label class="item-label" for="class-setting-update-remarks">描述：</label>
          <textarea class="item-textarea" id="class-setting-update-remarks" v-model="description"></textarea>
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
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'
import Time from '../../../../../../dependencies/modules/Time.class.js'

export default {
  name: 'ClassUpdateClassPanelComponent',
  data () {
    return {
      oid: 0,
      mid: 0,
      date: '',
      name: 0,
      manager: '',
      // school: '',
      teacher: 0,
      description: '',
      // college: '',
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
  created () {
    let panel = {...Communication.panel}
    this.data = {...Communication.panel}
    this.data.description = this.data.description
    this.oid = panel.oid
    this.mid = panel.mid
    this.manager = `${panel.manager.name}（${panel.manager.phone}）`
    this.name = panel.name
    this.data.date = `${Time.format('YYYY/MM/DD', panel.launch)} to ${Time.format('YYYY/MM/DD', panel.deadline)}`
    this.date = `${Time.format('YYYY/MM/DD', panel.launch)} to ${Time.format('YYYY/MM/DD', panel.deadline)}`
    // this.school = panel.school
    this.description = panel.description
  },
  methods: {
    selectTeacher () {
      Display.modal = 'teacher-select'
    },
    confirm () {
      let data = {oid: this.oid}

      if (this.data.name !== this.name) {
        if (!Check.appellation(this.name)) return
        data.name = this.name
      }
      if (this.data.mid !== this.mid) data.mid = this.mid
      // if (this.data.school !== this.school) data.school = this.school
      if (this.data.date !== this.date) {
        if (!Check.dateRange(this.date)) return
        data.launch = this.date.split(' to ')[0]
        data.deadline = this.date.split(' to ')[1]
      }
      if (this.teacher) data.teacher = this.teacher
      if (this.data.description !== this.description) data.description = this.description

      Http.send({
        url: 'UpdateClass',
        data: data
      }).before(() => {
        this.confirmDisabled = true
      }).success(data => {
        Display.api = 'ClassList'
      }).fail(data => {
      }).default(() => {
        this.confirmDisabled = false
        Display.panel = false
      })
    },
    cancel () {
      Display.panel = false
    }
  },
  watch: {
    '$store.state.modal' (modal, previous) {
      if (previous === 'teacher-select' && modal === false && Communication.modal) {
        this.manager = `${Communication.modal.name}（${Communication.modal.phone}）`
        this.teacher = {...Communication.modal}.user
      }
      // if (previous === 'school-select' && modal === false && Communication.modal) {
      //   this.college = `${Communication.modal.name}${Communication.modal.district}${Dictionary.rank[Communication.modal.level]}`
      //   this.school = {...Communication.modal}.school
      // }
    }
  },
  components: {
    // include chunk
    flatPickr
  }
}
</script>

<style lang="sass" scoped>
@import "./update-class.scss";
</style>
