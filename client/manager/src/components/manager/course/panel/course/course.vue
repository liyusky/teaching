<template>
  <!-- s  -->
  <section class="course">
    <div class="course-header">
      <p class="header-title">添加课程</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="course-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="course-setting-add-course-name">名称：</label>
          <input class="item-input" id="course-setting-add-course-name" type="text" v-model="name">
        </li>
        <li class="list-item">
          <label class="item-label" for="course-setting-add-course-language">语言：</label>
          <select class="item-select" id="course-setting-add-course-language" v-model="language">
            <option value="0">未定</option>
            <option value="1">综合</option>
            <option value="2">PASCAL</option>
            <option value="3">C</option>
            <option value="4" selected>C++</option>
          </select>
        </li>
        <li class="list-item">
          <label class="item-label" for="course-setting-add-course-grade">适用年级：</label>
          <select class="item-select" id="course-setting-add-course-grade" v-model="grade">
            <option value="0">未定</option>
            <option value="1">综合</option>
            <option value="2" selected>小学</option>
            <option value="3">初中</option>
            <option value="4">高中</option>
          </select>
        </li>
        <li class="list-item">
          <label class="item-label" for="course-setting-add-course-remarks">描述：</label>
          <textarea class="item-textarea" id="course-setting-add-course-remarks" v-model="description"></textarea>
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
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'CourseAddCoursePanelComponent',
  data () {
    return {
      name: '',
      language: 4,
      description: '',
      grade: 2,
      confirmDisabled: false
      // start datas
      // end datas
    }
  },
  methods: {
    confirm () {
      if (!Check.appellation(this.name)) return
      let data = {
        name: this.name,
        language: this.language,
        grade: this.grade
      }
      if (this.description) {
        data.description = this.description
      }
      Http.send({
        url: 'AddCourse',
        data: data
      }).success(data => {
        Display.api = 'CourseList'
      }).fail(data => {
        console.log(data)
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
      this.language = 3
      this.description = ''
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./course.scss";
</style>
