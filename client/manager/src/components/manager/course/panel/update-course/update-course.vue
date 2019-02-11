<template>
  <!-- s  -->
  <section class="update-course">
    <div class="course-header">
      <p class="header-title">
        <span class="title-main">修改课程信息</span>
        <span class="title-tip">（课程编号 {{cid}}）</span>
      </p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="course-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="course-setting-update-course-name">名称：</label>
          <input class="item-input" id="course-setting-update-course-name" type="text" v-model="name">
        </li>
        <li class="list-item">
          <label class="item-label" for="course-setting-update-course-language">语言：</label>
          <select class="item-select" id="course-setting-update-course-language" v-model="language">
            <option value="0">未定</option>
            <option value="1">综合</option>
            <option value="2">PASCAL</option>
            <option value="3">C</option>
            <option value="4">C++</option>
          </select>
        </li>
        <li class="list-item">
          <label class="item-label" for="course-setting-update-course-grade">适用年级：</label>
          <select class="item-select" id="course-setting-update-course-grade" v-model="grade">
            <option value="0">未定</option>
            <option value="1">综合</option>
            <option value="2">小学</option>
            <option value="3">初中</option>
            <option value="4">高中</option>
          </select>
        </li>
        <li class="list-item">
          <label class="item-label" for="course-setting-update-course-remarks">描述：</label>
          <textarea class="item-textarea" id="course-setting-update-course-remarks" v-model="description"></textarea>
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
  name: 'CourseUpdateCoursePanelComponent',
  data () {
    return {
      cid: 0,
      name: '',
      language: 3,
      grade: 2,
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
    this.cid = panel.cid
    this.grade = panel.grade
    this.name = panel.name
    this.language = panel.language
    this.description = panel.description
  },
  methods: {
    confirm () {
      let data = {
        cid: this.cid
      }

      if (this.data.name !== this.name) {
        if (!Check.appellation(this.name)) return
        data.name = this.name
      }

      if (this.data.grade !== this.grade) data.grade = this.grade
      if (this.data.language !== this.language) data.language = this.language
      if (this.data.description !== this.description) data.description = this.description

      Http.send({
        url: 'UpdateCourse',
        data: data
      }).before(() => {
        this.confirmDisabled = true
      }).success(data => {
        Display.api = 'CourseList'
      }).fail(data => {
        console.log(data)
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
@import "./update-course.scss";
</style>
