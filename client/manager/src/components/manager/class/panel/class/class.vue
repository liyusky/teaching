<template>
  <!-- s  -->
  <section class="class">
    <div class="class-header">
      <p class="header-title">添加班级</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="class-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="course-setting-add-name">班级名称：</label>
          <input class="item-input" id="course-setting-add-name" placeholder="不接受分号" type="text" v-model="name">
        </li>
        <li class="list-item">
          <label class="item-label" for="class-setting-add-manager">班主任：</label>
          <input class="item-input" id="class-setting-add-manager" type="text" readonly="readonly" v-model="manager" placeholder="请点击选择教师" @click="selectTeacher">
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="class-setting-add-school">学校：</label>
          <input class="item-input" id="class-setting-add-school" type="text" readonly="readonly" v-model="college" placeholder="请点击选择学生所属学校" @click="selectSchool" @keyup.enter="confirm" @keyup.esc="cancel">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="class-setting-add-date">开班时间：</label>
          <flat-pickr
            class="item-pickr"
            v-model="date"
            :config="config"
            :placeholder="'请选择开始时间，结束时间'"
            id="class-setting-add-date"></flat-pickr>
        </li>
        <li class="list-item">
          <label class="item-label" for="class-setting-add-remarks">描述：</label>
          <textarea class="item-textarea" id="class-setting-add-remarks" placeholder="请输入备注，可选" v-model="description"></textarea>
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
  name: 'ClassAddClassPanelComponent',
  data () {
    return {
      name: '',
      manager: '',
      mid: '',
      teacher: 0,
      description: '',
      // school: 1,
      date: '',
      config: {
        mode: 'range',
        wrap: true,
        altInput: true,
        altFormat: 'Y/m/d',
        dateFormat: 'Z'
      },
      // college: '',
      confirmDisabled: false
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
    flatPickr
  },
  methods: {
    selectTeacher () {
      Display.modal = 'teacher-select'
    },
    confirm () {
      if (!Check.appellation(this.name)) return
      if (!Check.dateRange(this.date)) return
      let data = {
        name: this.name,
        launch: this.date.split(' to ')[0],
        deadline: this.date.split(' to ')[1],
        teacher: this.teacher
      }
      if (this.description) data.description = this.description
      // if (this.school) data.school = this.school
      Http.send({
        url: 'AddClass',
        data: data
      }).success(data => {
        Display.api = 'ClassList'
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
      this.name = ''
      this.mid = ''
      this.description = ''
      // this.school = 1
      this.date = new Date()
    }
    // selectSchool () {
    //   Display.modal = 'school-select'
    // }
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
  }
}
</script>

<style lang="sass" scoped>
@import "./class.scss";
</style>
