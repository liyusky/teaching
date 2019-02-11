<template>
  <!-- s  -->
  <section class="update-homework">
    <div class="homework-header">
      <p class="header-title">
        <span class="title-main">修改作业信息</span>
        <span class="title-tip">（作业编号 {{hid}}）</span>
      </p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="homework-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="homework-setting-update-name">名称：</label>
          <input class="item-input" id="homework-setting-update-name" type="text" v-model="name">
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="homework-setting-update-lesson">课时编号：</label>
          <input class="item-input" id="homework-setting-update-lesson" type="text" v-model="lid">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="homework-setting-add-date">提交时间：</label>
          <flat-pickr
            class="item-pickr"
            v-model="date"
            :config="config"
            id="homework-setting-add-date"></flat-pickr>
        </li>
        <li class="list-item">
          <label class="item-label" for="homework-setting-update-remarks">描述：</label>
          <textarea class="item-textarea" id="homework-setting-update-remarks" v-model="description"></textarea>
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
  name: 'HomeworkUpdateHomeworkPanelComponent',
  data () {
    return {
      hid: 0,
      lid: 0,
      name: '',
      description: '',
      confirmDisabled: false,
      date: '',
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
  created () {
    let panel = {...Communication.panel}
    this.data = {...Communication.panel}
    this.data.date = `${Time.format('YYYY/MM/DD HH:mm', panel.launch)} to ${Time.format('YYYY/MM/DD HH:mm', panel.deadline)}`
    this.date = `${Time.format('YYYY/MM/DD HH:mm', panel.launch)} to ${Time.format('YYYY/MM/DD HH:mm', panel.deadline)}`
    this.data.description = this.data.description
    this.hid = panel.hid
    this.lid = panel.lid
    this.name = panel.name
    this.description = panel.description
  },
  components: {
    // include chunk
    flatPickr
  },
  methods: {
    confirm () {
      let data = {
        hid: this.hid
      }

      if (this.data.name !== this.name) {
        if (!Check.appellation(this.name)) return
        data.name = this.name
      }

      if (this.data.date !== this.date) {
        if (!Check.dateRange(this.date)) return
        data.launch = this.date.split(' to ')[0]
        data.deadline = this.date.split(' to ')[1]
      }

      // if (this.data.lid !== this.lid) data.lid = this.lid
      if (this.data.description !== this.description) data.description = this.description

      Http.send({
        url: 'UpdateHomework',
        data: data
      }).before(() => {
        this.confirmDisabled = true
      }).success(data => {
        Display.api = 'HomeworkList'
      }).fail(data => {
      }).default(() => {
        this.confirmDisabled = false
        Display.panel = false
      })
    },
    cancel () {
      Display.panel = false
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./update-homework.scss";
</style>
