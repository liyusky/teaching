<template>
  <!-- s  -->
  <section class="update-lesson">
    <div class="lesson-header">
      <p class="header-title">
        <span class="title-main">修改课时信息</span>
        <span class="title-tip">（课时编号 {{lid}}）</span>
      </p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="lesson-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="lesson-setting-update-lesson-name">名称：</label>
          <input class="item-input" id="lesson-setting-update-lesson-name" type="text" v-model="name">
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="lesson-setting-update-lesson-course">课程编号：</label>
          <input class="item-input" id="lesson-setting-update-lesson-course" type="text" v-model="cid">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="lesson-setting-update-lesson-remarks">描述：</label>
          <textarea class="item-textarea" id="lesson-setting-update-lesson-remarks" v-model="description"></textarea>
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
// include dependence
import Check from '../../../../../../dependencies/modules/Check.class.js'
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'LessonUpdateLessonPanelComponent',
  data () {
    return {
      cid: 0,
      lid: 0,
      name: '',
      description: '',
      confirmDisabled: false
      // start datas
      // end datas
    }
  },
  created () {
    let panel = {...Communication.panel}
    this.data = {...Communication.panel}
    this.data.description = this.data.description
    this.lid = panel.lid
    this.cid = panel.cid
    this.name = panel.name
    this.description = panel.description
  },
  methods: {
    confirm () {
      let data = {
        lid: this.lid
      }

      if (this.data.name !== this.name) {
        if (!Check.appellation(this.name)) return
        data.name = this.name
      }
      // if (this.data.cid !== this.cid) data.cid = this.cid
      if (this.data.description !== this.description) data.description = this.description

      Http.send({
        url: 'UpdateLesson',
        data: data
      }).before(() => {
        this.confirmDisabled = true
      }).success(data => {
        Display.api = 'LessonList'
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
@import "./update-lesson.scss";
</style>
