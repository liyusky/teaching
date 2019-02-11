<template>
  <!-- s  -->
  <section class="lesson">
    <div class="lesson-header">
      <p class="header-title">
        <span class="title-name">添加课时</span>
      </p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="lesson-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="lesson-setting-add-lesson-name">名称：</label>
          <input class="item-input" id="lesson-setting-add-lesson-name" type="text" v-model="name">
        </li>
        <li class="list-item">
          <label class="item-label" for="lesson-setting-add-lesson-remarks">描述：</label>
          <textarea class="item-textarea" id="lesson-setting-add-lesson-remarks" v-model="description"></textarea>
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
// import Account from '../../../../../../dependencies/modules/Account.class.js'
import Check from '../../../../../../dependencies/modules/Check.class.js'
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'LessonAddLessonPanelComponent',
  data () {
    return {
      name: '',
      description: ''
      // start datas
      // end datas
    }
  },
  methods: {
    confirm () {
      if (!Check.appellation(this.name)) return
      let data = {
        name: this.name,
        cid: Communication.panel.cid,
        course: Communication.panel.cid
      }
      if (this.description) {
        data.description = this.description
      }
      Http.send({
        url: 'AddLesson',
        data: data
      }).success(data => {
        Display.api = 'LessonList'
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
      this.description = ''
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./lesson.scss";
</style>
