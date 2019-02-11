
<template>
  <!-- s  -->
  <section class="homework">
    <div class="homework-header">
      <p class="header-title">添加作业</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="homework-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="homework-setting-add-name">名称：</label>
          <input class="item-input" id="homework-setting-add-name" type="text" v-model="name">
        </li>
        <li class="list-item">
          <label class="item-label" for="homework-setting-add-date">提交时间：</label>
          <flat-pickr
            class="item-pickr"
            v-model="date"
            :config="config"
            id="homework-setting-add-date"></flat-pickr>
        </li>
        <li class="list-item">
          <label class="item-label" for="student-setting-student-remarks">描述：</label>
          <textarea class="item-textarea" id="student-setting-student-remarks" v-model="description"></textarea>
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
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'HomeworkAddHomeworkPanelComponent',
  data () {
    return {
      name: '',
      date: '',
      description: '',
      config: {
        mode: 'range',
        enableTime: true,
        wrap: true,
        altInput: true,
        altFormat: 'Y/m/d H:i',
        dateFormat: 'Z'
      }
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
    flatPickr
  },
  methods: {
    getLaunch () {
    },
    getDeadline () {
    },
    confirm () {
      if (!Check.appellation(this.name)) return
      if (!Check.dateRange(this.date)) return
      let data = {
        name: this.name,
        curid: Communication.panel.curid,
        curriculum: Communication.panel.curid,
        task: 1,
        launch: this.date.split(' to ')[0],
        deadline: this.date.split(' to ')[1]
      }
      if (this.description) data.description = this.description
      Http.send({
        url: 'AddHomework',
        data: data
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
      this.clear()
    },
    clear () {
      this.name = ''
      this.launch = ''
      this.deadline = ''
      this.description = ''
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./homework.scss";
</style>
